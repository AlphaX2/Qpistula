# Copyright (c) 2012, Menno Smits
# Released subject to the New BSD License
# Please see http://en.wikipedia.org/wiki/BSD_licenses

import itertools
import socket
import sys
from datetime import datetime
from StringIO import StringIO
from imapclient.fixed_offset import FixedOffset
from imapclient.imapclient import datetime_to_imap
from imapclient.test.mock import patch, sentinel, Mock
from imapclient.test.testable_imapclient import TestableIMAPClient as IMAPClient
from imapclient.test.util import unittest

class IMAPClientTest(unittest.TestCase):

    def setUp(self):
        self.client = IMAPClient()


class TestListFolders(IMAPClientTest):

    def test_list_folders(self):
        self.client._imap._simple_command.return_value = ('OK', 'something')
        self.client._imap._untagged_response.return_value = ('LIST', sentinel.folder_data)
        self.client._proc_folder_list = Mock(return_value=sentinel.folder_list)

        folders = self.client.list_folders(sentinel.dir, sentinel.pattern)

        self.assertEqual(self.client._imap._simple_command.call_args, (('LIST', sentinel.dir, sentinel.pattern), {}))
        self.assertEqual(self.client._proc_folder_list.call_args, ((sentinel.folder_data,), {}))
        self.assert_(folders is sentinel.folder_list)

    def test_list_sub_folders(self):
        self.client._imap._simple_command.return_value = ('OK', 'something')
        self.client._imap._untagged_response.return_value = ('LSUB', sentinel.folder_data)
        self.client._proc_folder_list = Mock(return_value=sentinel.folder_list)

        folders = self.client.list_sub_folders(sentinel.dir, sentinel.pattern)

        self.assert_(self.client._imap._simple_command.call_args == (('LSUB', sentinel.dir, sentinel.pattern), {}))
        self.assert_(self.client._proc_folder_list.call_args == ((sentinel.folder_data,), {}))
        self.assert_(folders is sentinel.folder_list)


    def test_list_folders_NO(self):
        self.client._imap._simple_command.return_value = ('NO', ['badness'])
        self.assertRaises(IMAPClient.Error, self.client.list_folders)


    def test_list_sub_folders_NO(self):
        self.client._imap._simple_command.return_value = ('NO', ['badness'])
        self.assertRaises(IMAPClient.Error, self.client.list_folders)


    def test_simple(self):
        folders = self.client._proc_folder_list(['(\\HasNoChildren) "/" "A"',
                                                 '(\\HasNoChildren) "/" "Foo Bar"',
                                                 ])
        self.assertEqual(folders, [(['\\HasNoChildren'], '/', 'A',),
                                   (['\\HasNoChildren'], '/', 'Foo Bar')])


    def test_without_quotes(self):
        folders = self.client._proc_folder_list(['(\\HasNoChildren) "/" A',
                                                 '(\\HasNoChildren) "/" B',
                                                 '(\\HasNoChildren) "/" C',
                                                 ])
        self.assertEqual(folders, [(['\\HasNoChildren'], '/', 'A'),
                                   (['\\HasNoChildren'], '/', 'B'),
                                   (['\\HasNoChildren'], '/', 'C')])

    def test_unquoted_numeric_folder_name(self):
        # Some IMAP implementations do this
        folders = self.client._proc_folder_list(['(\\HasNoChildren) "/" 123'])
        self.assertEqual(folders, [(['\\HasNoChildren'], '/', '123')])

    def test_mixed(self):
        folders = self.client._proc_folder_list(['(\\HasNoChildren) "/" Alpha',
                                                 '(\\HasNoChildren) "/" "Foo Bar"',
                                                 '(\\HasNoChildren) "/" C',
                                                 ])
        self.assertEqual(folders, [(['\\HasNoChildren'], '/', 'Alpha'),
                                   (['\\HasNoChildren'], '/', 'Foo Bar'),
                                   (['\\HasNoChildren'], '/', 'C')])


    def test_funky_characters(self):
        folders = self.client._proc_folder_list([('(\\NoInferiors \\UnMarked) "/" {5}', 'bang\xff'),
                                                 '',
                                                 '(\\HasNoChildren \\UnMarked) "/" "INBOX"'])
        self.assertEqual(folders, [(['\\NoInferiors', '\\UnMarked'], "/", u'bang\xff'),
                                   (['\\HasNoChildren', '\\UnMarked'], "/", u'INBOX')])


    def test_quoted_specials(self):
        folders = self.client._proc_folder_list([r'(\HasNoChildren) "/" "Test \"Folder\""',
                                                 r'(\HasNoChildren) "/" "Left\"Right"',
                                                 r'(\HasNoChildren) "/" "Left\\Right"',
                                                 r'(\HasNoChildren) "/" "\"Left Right\""',
                                                 r'(\HasNoChildren) "/" "\"Left\\Right\""',
                                                 ])
        self.assertEqual(folders, [(['\\HasNoChildren'], '/', 'Test "Folder"'),
                                   (['\\HasNoChildren'], '/', 'Left\"Right'),
                                   (['\\HasNoChildren'], '/', r'Left\Right'),
                                   (['\\HasNoChildren'], '/', r'"Left Right"'),
                                   (['\\HasNoChildren'], '/', r'"Left\Right"'),
                                   ])

    def test_empty_response(self):
        self.assertEqual(self.client._proc_folder_list([None]), [])


    def test_blanks(self):
        folders = self.client._proc_folder_list(['', None, r'(\HasNoChildren) "/" "last"'])
        self.assertEqual(folders, [([r'\HasNoChildren'], '/', 'last')])


class TestAppend(IMAPClientTest):

    def test_without_msg_time(self):
        self.client._imap.append.return_value = ('OK', ['Good'])

        self.client.append('foobar', sentinel.msg, ['FLAG', 'WAVE'], None)

        self.assert_(self.client._imap.method_calls ==
                     [('append', ('"foobar"',
                                  '(FLAG WAVE)',
                                  None,
                                  sentinel.msg),
                                 {})
                      ])

    @patch('imapclient.imapclient.datetime_to_imap')
    def test_with_msg_time(self, datetime_to_imap):
        datetime_to_imap.return_value = 'somedate'
        self.client._imap.append.return_value = ('OK', ['Good'])

        self.client.append('foobar', sentinel.msg, ['FLAG', 'WAVE'],
                           datetime(2009, 4, 5, 11, 0, 5, 0, FixedOffset(2*60)))

        self.assert_(datetime_to_imap.called)
        self.assert_(self.client._imap.method_calls ==
                     [('append', ('"foobar"',
                                  '(FLAG WAVE)',
                                  '"somedate"',
                                  sentinel.msg),
                                 {})
                      ])


class TestDateTimeToImap(unittest.TestCase):

    def test_with_timezone(self):
        dt = datetime(2009, 1, 2, 3, 4, 5, 0, FixedOffset(2*60 + 30))
        self.assert_(datetime_to_imap(dt) == '02-Jan-2009 03:04:05 +0230')

    @patch('imapclient.imapclient.FixedOffset.for_system')
    def test_without_timezone(self, for_system):
        dt = datetime(2009, 1, 2, 3, 4, 5, 0)
        for_system.return_value = FixedOffset(-5 * 60)

        self.assert_(datetime_to_imap(dt) == '02-Jan-2009 03:04:05 -0500')


class TestAclMethods(IMAPClientTest):

    def test_getacl(self):
        self.client._imap.getacl.return_value = ('OK', ['INBOX Fred rwipslda Sally rwip'])
        acl = self.client.getacl('INBOX')
        self.assertSequenceEqual(acl, [('Fred', 'rwipslda'), ('Sally', 'rwip')])

    def test_setacl(self):
        self.client._imap.setacl.return_value = ('OK', ["SETACL done"])

        response = self.client.setacl(u'folder', sentinel.who, sentinel.what)

        self.client._imap.setacl.assert_called_with('"folder"', sentinel.who, sentinel.what)
        self.assertEqual(response, "SETACL done")


class TestIdleAndNoop(IMAPClientTest):

    def test_idle(self):
        self.client._imap._command.return_value = sentinel.tag
        self.client._imap._get_response.return_value = None

        self.client.idle()

        self.client._imap._command.assert_called_with('IDLE')
        self.assertEqual(self.client._idle_tag, sentinel.tag)

    @patch('imapclient.imapclient.select.select')
    def test_idle_check_blocking(self, mock_select):
        mock_sock = Mock()
        self.client._imap.sock = mock_sock
        mock_select.return_value = ([True], [], [])
        counter = itertools.count()
        def fake_get_line():
            count = counter.next()
            if count == 0:
                return '* 1 EXISTS'
            elif count == 1:
                return '* 0 EXPUNGE'
            else:
                raise socket.timeout
        self.client._imap._get_line = fake_get_line

        responses = self.client.idle_check()

        mock_select.assert_called_once_with([mock_sock], [], [], None)
        self.assertListEqual(mock_sock.method_calls,
                             [('setblocking', (0,), {}),
                              ('setblocking', (1,), {})])
        self.assertListEqual([(1, 'EXISTS'), (0, 'EXPUNGE')], responses)

    @patch('imapclient.imapclient.select.select')
    def test_idle_check_timeout(self, mock_select):
        mock_sock = Mock()
        self.client._imap.sock = mock_sock
        mock_select.return_value = ([], [], [])

        responses = self.client.idle_check(timeout=0.5)

        mock_select.assert_called_once_with([mock_sock], [], [], 0.5)
        self.assertListEqual(mock_sock.method_calls,
                             [('setblocking', (0,), {}),
                              ('setblocking', (1,), {})])
        self.assertListEqual([], responses)

    @patch('imapclient.imapclient.select.select')
    def test_idle_check_with_data(self, mock_select):
        mock_sock = Mock()
        self.client._imap.sock = mock_sock
        mock_select.return_value = ([True], [], [])
        counter = itertools.count()
        def fake_get_line():
            count = counter.next()
            if count == 0:
                return '* 99 EXISTS'
            else:
                raise socket.timeout
        self.client._imap._get_line = fake_get_line
            
        responses = self.client.idle_check()

        mock_select.assert_called_once_with([mock_sock], [], [], None)
        self.assertListEqual(mock_sock.method_calls,
                             [('setblocking', (0,), {}),
                              ('setblocking', (1,), {})])
        self.assertListEqual([(99, 'EXISTS')], responses)

    def test_idle_done(self):
        self.client._idle_tag = sentinel.tag

        mockSend = Mock()
        self.client._imap.send = mockSend
        mockConsume = Mock(return_value=sentinel.out)
        self.client._consume_until_tagged_response = mockConsume

        result = self.client.idle_done()

        mockSend.assert_called_with('DONE\r\n')
        mockConsume.assert_called_with(sentinel.tag, 'IDLE')
        self.assertEquals(result, sentinel.out)

    def test_noop(self):
        mockCommand = Mock(return_value=sentinel.tag)
        self.client._imap._command = mockCommand
        mockConsume = Mock(return_value=sentinel.out)
        self.client._consume_until_tagged_response = mockConsume

        result = self.client.noop()

        mockCommand.assert_called_with('NOOP')
        mockConsume.assert_called_with(sentinel.tag, 'NOOP')
        self.assertEquals(result, sentinel.out)

    def test_consume_until_tagged_response(self):
        client = self.client
        client._imap.tagged_commands = {sentinel.tag: None}

        counter = itertools.count()
        def fake_get_response():
            count = counter.next()
            if count == 0:
                return '* 99 EXISTS'
            client._imap.tagged_commands[sentinel.tag] = ('OK', ['Idle done'])
        client._imap._get_response = fake_get_response
            
        text, responses = client._consume_until_tagged_response(sentinel.tag,
                                                                'IDLE')
        self.assertEqual(client._imap.tagged_commands, {})
        self.assertEqual(text, 'Idle done')
        self.assertListEqual([(99, 'EXISTS')], responses)


                         
class TestDebugLogging(IMAPClientTest):

    def test_default_is_stderr(self):
        self.assertIs(self.client.log_file, sys.stderr)

    def test_IMAP_is_patched(self):
        log = StringIO()
        self.client.log_file = log

        self.client._log('one')
        self.client._imap._mesg('two')

        output = log.getvalue()
        self.assertIn('one', output)
        self.assertIn('two', output)

class TestTimeNormalisation(IMAPClientTest):

    def test_default(self):
        self.assertTrue(self.client.normalise_times)

    @patch('imapclient.imapclient.parse_fetch_response')
    def test_pass_through(self, parse_fetch_response):
        self.client._imap._command_complete.return_value = ('OK', sentinel.data)
        self.client._imap._untagged_response.return_value = ('OK', sentinel.fetch_data)
        self.client.use_uid = sentinel.use_uid

        def check(expected):
            self.client.fetch(22, ['SOMETHING'])
            parse_fetch_response.assert_called_with(sentinel.fetch_data,
                                                    expected,
                                                    sentinel.use_uid)

        self.client.normalise_times = True
        check(True)

        self.client.normalise_times = False
        check(False)


class TestGmailLabels(IMAPClientTest):

    def setUp(self):
        super(TestGmailLabels, self).setUp()
        patcher = patch.object(self.client, '_store', autospec=True, return_value=sentinel.label_set)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_get(self):
        with patch.object(self.client, 'fetch', autospec=True,
                          return_value={123: {'X-GM-LABELS': ['foo', 'bar']},
                                        444: {'X-GM-LABELS': ['foo']}}):
            out = self.client.get_gmail_labels(sentinel.messages)
            self.client.fetch.assert_called_with(sentinel.messages, ['X-GM-LABELS'])
            self.assertEquals(out, {123: ['foo', 'bar'],
                                    444: ['foo']})

    def test_add(self):
        self.client.add_gmail_labels(sentinel.messages, sentinel.labels)
        self.client._store.assert_called_with('+X-GM-LABELS', sentinel.messages, sentinel.labels)

    def test_remove(self):
        self.client.remove_gmail_labels(sentinel.messages, sentinel.labels)
        self.client._store.assert_called_with('-X-GM-LABELS', sentinel.messages, sentinel.labels)

    def test_set(self):
        self.client.set_gmail_labels(sentinel.messages, sentinel.labels)
        self.client._store.assert_called_with('X-GM-LABELS', sentinel.messages, sentinel.labels)


class TestNamespace(IMAPClientTest):

    def set_return(self, value):
        self.client._imap.namespace.return_value = ('OK', [value])

    def test_simple(self):
        self.set_return('(("FOO." "/")) NIL NIL')
        self.assertEquals(self.client.namespace(), ((('FOO.', '/'),), None, None))

    def test_other_only(self):
        self.set_return('NIL NIL (("" "."))')
        self.assertEquals(self.client.namespace(), (None, None, (("", "."),)))

    def test_complex(self):
        self.set_return('(("" "/")) '
                        '(("~" "/")) '
                        '(("#shared/" "/") ("#public/" "/")("#ftp/" "/")("#news." "."))')
        self.assertEquals(self.client.namespace(), (
            (("", "/"),),
            (("~", "/"),),
            (("#shared/", "/"), ("#public/", "/"), ("#ftp/", "/"), ("#news.", ".")),
            ))


if __name__ == '__main__':
    unittest.main()
