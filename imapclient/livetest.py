#!/usr/bin/python

# Copyright (c) 2012, Menno Smits
# Released subject to the New BSD License
# Please see http://en.wikipedia.org/wiki/BSD_licenses


import imp
import os
import sys
import time
from datetime import datetime
from email.utils import make_msgid

import imapclient
from test.util import unittest
from config import parse_config_file, create_client_from_config

# TODO cleaner verbose output: avoid "__main__" and separator between classes


SIMPLE_MESSAGE = 'Subject: something\r\n\r\nFoo\r\n'

# Simple address in To header triggers interesting Fastmail.fm
# behaviour with ENVELOPE responses.
MULTIPART_MESSAGE = """\
From: Bob Smith <bob@smith.com>
To: Some One <some@one.com>, foo@foo.com
Date: Tue, 16 Mar 2010 16:45:32 +0000
MIME-Version: 1.0
Subject: A multipart message
Content-Type: multipart/mixed; boundary="===============1534046211=="

--===============1534046211==
Content-Type: text/html; charset="us-ascii"
Content-Transfer-Encoding: quoted-printable

<html><body>
Here is the first part.
</body></html>

--===============1534046211==
Content-Type: text/plain; charset="us-ascii"
Content-Transfer-Encoding: 7bit

Here is the second part.

--===============1534046211==--
""".replace('\n', '\r\n')


def createLiveTestClass(conf, use_uid):

    class LiveTest(unittest.TestCase):

        def setUp(self):
            self.client = create_client_from_config(conf)
            self.client.use_uid = use_uid
            self.base_folder = conf.namespace[0] + ('__imapclient')
            self.folder_delimiter = conf.namespace[1]
            self.clear_test_folders()
            self.unsub_all_test_folders()
            self.client.create_folder(self.base_folder)
            self.client.select_folder(self.base_folder)

        def tearDown(self):
            self.clear_test_folders()
            self.unsub_all_test_folders()
            self.client.logout()

        def skip_unless_capable(self, capability, name=None):
            if not self.client.has_capability(capability):
                if not name:
                    name = capability
                self.skipTest("Server doesn't support %s" % name)

        def just_folder_names(self, dat):
            ret = []
            for _, _, folder_name in dat:
                # gmail's "special" folders start with '['
                if not folder_name.startswith('['):
                    ret.append(folder_name)
            return ret

        def all_test_folder_names(self):
            return self.just_folder_names(self.client.list_folders(self.base_folder))

        def all_sub_test_folder_names(self):
            return self.just_folder_names(self.client.list_sub_folders(self.base_folder))

        def clear_test_folders(self):
            self.client.folder_encode = False

            # Sort folders depth first because some implementations
            # (e.g. MS Exchange) will delete child folders when a
            # parent is deleted.
            def get_folder_depth(folder):
                return folder.count(self.folder_delimiter)
            folder_names = sorted(self.all_test_folder_names(),
                                  key=get_folder_depth,
                                  reverse=True)
            for folder in folder_names:
                self.client.delete_folder(folder)
            self.client.folder_encode = True

        def clear_folder(self, folder):
            self.client.select_folder(folder)
            self.client.delete_messages(self.client.search())
            self.client.expunge()

        def add_prefix_to_folder(self, folder):
            return self.base_folder + self.folder_delimiter + folder

        def add_prefix_to_folders(self, folders):
            return [self.add_prefix_to_folder(folder) for folder in folders]

        def unsub_all_test_folders(self):
            for folder in self.all_sub_test_folder_names():
                self.client.unsubscribe_folder(folder)

        def is_gmail(self):
            return self.client._imap.host == 'imap.gmail.com'

        def is_fastmail(self):
            return self.client._imap.host == 'mail.messagingengine.com'

        def is_exchange(self):
            # Assume that these capabilities mean we're talking to MS
            # Exchange. A bit of a guess really.
            return (self.client.has_capability('IMAP4') and
                    self.client.has_capability('AUTH=NTLM') and
                    self.client.has_capability('AUTH=GSSAPI'))

        def test_capabilities(self):
            caps = self.client.capabilities()
            self.assertIsInstance(caps, tuple)
            self.assertGreater(len(caps), 1)
            for cap in caps:
                self.assertTrue(self.client.has_capability(cap))
            self.assertFalse(self.client.has_capability('WONT EXIST'))

        def test_namespace(self):
            self.skip_unless_capable('NAMESPACE')

            def assertNoneOrTuple(val):
                assert val is None or isinstance(val, tuple), \
                       "unexpected namespace value %r" % val

            ns = self.client.namespace()
            self.assertEqual(len(ns), 3)
            assertNoneOrTuple(ns.personal)
            assertNoneOrTuple(ns.other)
            assertNoneOrTuple(ns.shared)
            self.assertEqual(ns.personal, ns[0])
            self.assertEqual(ns.other, ns[1])
            self.assertEqual(ns.shared, ns[2])

        def test_select_and_close(self):
            resp = self.client.select_folder(self.base_folder)
            self.assertEqual(resp['EXISTS'], 0)
            self.assertIsInstance(resp['RECENT'], int)
            self.assertIsInstance(resp['FLAGS'], tuple)
            self.assertGreater(len(resp['FLAGS']), 1)
            self.client.close_folder()

        def test_select_read_only(self):
            self.client.append(self.base_folder, SIMPLE_MESSAGE)
            self.assertNotIn('READ-ONLY', self.client._imap.untagged_responses)

            resp = self.client.select_folder(self.base_folder, readonly=True)

            self.assertIn('READ-ONLY', self.client._imap.untagged_responses)
            self.assertEqual(resp['EXISTS'], 1)
            self.assertIsInstance(resp['RECENT'], int)
            self.assertIsInstance(resp['FLAGS'], tuple)
            self.assertGreater(len(resp['FLAGS']), 1)

        def test_list_folders(self):
            some_folders = ['simple', u'L\xffR']
            if not self.is_fastmail():
                some_folders.extend([r'test"folder"', r'foo\bar'])
            some_folders = self.add_prefix_to_folders(some_folders)
            for name in some_folders:
                self.client.create_folder(name)

            folders = self.all_test_folder_names()
            self.assertGreater(len(folders), 1, 'No folders visible on server')
            self.assertIn(self.base_folder, folders)

            for name in some_folders:
                self.assertIn(name, folders)

            #TODO: test LIST with wildcards

        def test_gmail_xlist(self):
            caps = self.client.capabilities()
            if self.is_gmail():
                self.assertIn("XLIST", caps, "expected XLIST in Gmail's capabilities")

        def test_xlist(self):
            self.skip_unless_capable('XLIST')

            result = self.client.xlist_folders()
            self.assertGreater(len(result), 0, 'No folders returned by XLIST')
            for flags, _, _  in result:
                if '\\INBOX' in [flag.upper() for flag in flags]:
                    break
                else:
                    self.fail('INBOX not returned in XLIST output')

        def test_subscriptions(self):
            test_folders = self.add_prefix_to_folders(['foobar', 'stuff & things', u'test & \u2622'])
            for folder in test_folders:
                self.client.create_folder(folder)

            all_folders = sorted(self.all_test_folder_names())
            for folder in all_folders:
                self.client.subscribe_folder(folder)

            self.assertListEqual(all_folders, sorted(self.all_sub_test_folder_names()))

            for folder in all_folders:
                self.client.unsubscribe_folder(folder)
            self.assertListEqual(self.all_sub_test_folder_names(), [])

            # Exchange doesn't return an error when subscribing to a
            # non-existent folder
            if not self.is_exchange():
                self.assertRaises(imapclient.IMAPClient.Error,
                                  self.client.subscribe_folder,
                                  'this folder is not likely to exist')

        def test_folders(self):
            self.assertTrue(self.client.folder_exists(self.base_folder))
            self.assertFalse(self.client.folder_exists('this is very unlikely to exist'))

            test_folders = ['foobar',
                            'stuff & things',
                            u'test & \u2622',
                            '123']

            if not self.is_fastmail():
                # Fastmail doesn't appear like double quotes in folder names
                test_folders.extend(['"foobar"', 'foo "bar"'])

            test_folders = self.add_prefix_to_folders(test_folders)

            for folder in test_folders:
                self.assertFalse(self.client.folder_exists(folder))

                self.client.create_folder(folder)

                self.assertTrue(self.client.folder_exists(folder))
                self.assertIn(folder, self.all_test_folder_names())

                self.client.select_folder(folder)
                self.client.close_folder()

                self.client.delete_folder(folder)
                self.assertFalse(self.client.folder_exists(folder))

        def test_rename_folder(self):
            test_folders = self.add_prefix_to_folders([
                'foobar',
                'stuff & things',
                u'test & \u2622',
                '123'])
            for folder in test_folders:
                self.client.create_folder(folder)

                new_folder = folder + 'x'
                resp = self.client.rename_folder(folder, new_folder)
                self.assertIsInstance(resp, str)
                self.assertTrue(len(resp) > 0)

                self.assertFalse(self.client.folder_exists(folder))
                self.assertTrue(self.client.folder_exists(new_folder))

        def test_status(self):
            # Default behaviour should return 5 keys
            self.assertEqual(len(self.client.folder_status(self.base_folder)), 5)

            new_folder = self.add_prefix_to_folder(u'test \u2622')
            self.client.create_folder(new_folder)
            try:
                status = self.client.folder_status(new_folder)
                self.assertEqual(status['MESSAGES'], 0)
                self.assertEqual(status['RECENT'], 0)
                self.assertEqual(status['UNSEEN'], 0)

                # Add a message to the folder, it should show up now.
                self.client.append(new_folder, SIMPLE_MESSAGE)

                status = self.client.folder_status(new_folder)
                self.assertEqual(status['MESSAGES'], 1)
                if not self.is_gmail():
                    self.assertEqual(status['RECENT'], 1)
                self.assertEqual(status['UNSEEN'], 1)
            finally:
                self.client.delete_folder(new_folder)

        def test_append(self):
            # Message time microseconds are set to 0 because the server will return
            # time with only seconds precision.
            msg_time = datetime.now().replace(microsecond=0)

            # Append message
            resp = self.client.append(self.base_folder, SIMPLE_MESSAGE, ('abc', 'def'), msg_time)
            self.assertIsInstance(resp, str)

            # Retrieve the just added message and check that all looks well
            self.assertEqual(self.client.select_folder(self.base_folder)['EXISTS'], 1)

            resp = self.client.fetch(self.client.search()[0], ('RFC822', 'FLAGS', 'INTERNALDATE'))

            self.assertEqual(len(resp), 1)
            msginfo = resp.values()[0]

            # Time should match the time we specified
            returned_msg_time = msginfo['INTERNALDATE']
            self.assertIsNone(returned_msg_time.tzinfo)
            self.assertEqual(returned_msg_time, msg_time)

            # Flags should be the same
            self.assertIn('abc', msginfo['FLAGS'])
            self.assertIn('def', msginfo['FLAGS'])

            # Message body should match
            self.assertEqual(msginfo['RFC822'], SIMPLE_MESSAGE)

        def test_flags(self):
            self.client.append(self.base_folder, SIMPLE_MESSAGE)
            msg_id = self.client.search()[0]

            def _flagtest(func, args, expected_flags):
                answer = func(msg_id, *args)
                self.assertTrue(answer.has_key(msg_id))
                answer_flags = set(answer[msg_id])
                answer_flags.discard(r'\Recent')  # Might be present but don't care
                self.assertSetEqual(answer_flags, set(expected_flags))

            base_flags = ['abc', 'def']
            _flagtest(self.client.set_flags, [base_flags], base_flags)
            _flagtest(self.client.get_flags, [], base_flags)
            _flagtest(self.client.add_flags, ['boo'], base_flags + ['boo'])
            _flagtest(self.client.remove_flags, ['boo'], base_flags)

        def test_gmail_labels(self):
            self.skip_unless_capable('X-GM-EXT-1', 'labels')

            self.client.append(self.base_folder, SIMPLE_MESSAGE)
            msg_id = self.client.search()[0]

            def _labeltest(func, args, expected_labels):
                answer = func(msg_id, *args)
                self.assertEquals(answer.keys(), [msg_id])
                actual_labels = set(answer[msg_id])
                self.assertSetEqual(actual_labels, set(expected_labels))

            base_labels = ['_imapclient_foo', '_imapclient_bar']
            try:
                _labeltest(self.client.set_gmail_labels, [base_labels], base_labels)
                _labeltest(self.client.get_gmail_labels, [], base_labels)
                _labeltest(self.client.add_gmail_labels, ['_imapclient_baz'], base_labels + ['_imapclient_baz'])
                _labeltest(self.client.remove_gmail_labels, ['_imapclient_baz'], base_labels)
            finally:
                # Clean up
                for label in ['_imapclient_baz'] + base_labels:
                    if self.client.folder_exists(label):
                        self.client.delete_folder(label)

        def test_search(self):
            # Add some test messages
            msg_tmpl = 'Subject: %s\r\n\r\nBody'
            subjects = ('a', 'b', 'c')
            for subject in subjects:
                msg = msg_tmpl % subject
                if subject == 'c':
                    flags = (imapclient.DELETED,)
                else:
                    flags = ()
                self.client.append(self.base_folder, msg, flags)

            # Check we see all messages
            messages_all = self.client.search('ALL')
            if self.is_gmail():
                # Gmail seems to never return deleted items.
                self.assertEqual(len(messages_all), len(subjects) - 1)
            else:
                self.assertEqual(len(messages_all), len(subjects))
            self.assertListEqual(self.client.search(), messages_all)      # Check default

            # Single criteria
            if not self.is_gmail():
                self.assertEqual(len(self.client.search('DELETED')), 1)
                self.assertEqual(len(self.client.search('NOT DELETED')), len(subjects) - 1)
            self.assertListEqual(self.client.search('NOT DELETED'), self.client.search(['NOT DELETED']))

            # Multiple criteria
            self.assertEqual(len(self.client.search(['NOT DELETED', 'SMALLER 500'])), len(subjects) - 1)
            self.assertEqual(len(self.client.search(['NOT DELETED', 'SUBJECT "a"'])), 1)
            self.assertEqual(len(self.client.search(['NOT DELETED', 'SUBJECT "c"'])), 0)

        def test_sort(self):
            if not self.client.has_capability('SORT'):
                return self.skipTest("Server doesn't support SORT")

            # Add some test messages
            msg_tmpl = 'Subject: Test\r\n\r\nBody'
            num_lines = (10, 20, 30)
            line = '\n' + ('x' * 72)
            for line_cnt in num_lines:
                msg = msg_tmpl + (line * line_cnt)
                self.client.append(self.base_folder, msg)

            messages = self.client.sort('REVERSE SIZE')
            self.assertEqual(len(messages), 3)
            first_id = messages[0]
            expected = [first_id, first_id - 1, first_id - 2]
            self.assertListEqual(messages, expected)

        def test_copy(self):
            self.client.append(self.base_folder, SIMPLE_MESSAGE)
            target_folder = self.add_prefix_to_folder('target')
            self.client.create_folder(target_folder)
            msg_id = self.client.search()[0]

            self.client.copy(msg_id, target_folder)

            self.client.select_folder(target_folder)
            msgs = self.client.search()
            self.assertEqual(len(msgs), 1)
            msg_id = msgs[0]
            self.assertIn('something', self.client.fetch(msg_id, ['RFC822'])[msg_id]['RFC822'])

        def test_fetch(self):
            # Generate a fresh message-id each time because Gmail is
            # clever and will treat appends of messages with
            # previously seen message-ids as the same message. This
            # breaks our tests when the test message is updated.
            msg_id_header = make_msgid()
            msg = ('Message-ID: %s\r\n' % msg_id_header) + MULTIPART_MESSAGE

            self.client.select_folder(self.base_folder)
            self.client.append(self.base_folder, msg)

            fields = ['RFC822', 'FLAGS', 'INTERNALDATE', 'ENVELOPE']
            msg_id = self.client.search()[0]
            resp = self.client.fetch(msg_id, fields)

            self.assertEqual(len(resp), 1)
            msginfo = resp[msg_id]

            self.assertSetEqual(set(msginfo.keys()), set(fields + ['SEQ']))
            self.assertEqual(msginfo['SEQ'], 1)
            self.assertMultiLineEqual(msginfo['RFC822'], msg)
            self.assertIsInstance(msginfo['INTERNALDATE'], datetime)
            self.assertIsInstance(msginfo['FLAGS'], tuple)
            self.assertTupleEqual(msginfo['ENVELOPE'],
                                  ('Tue, 16 Mar 2010 16:45:32 +0000',
                                   'A multipart message',
                                   (('Bob Smith', None, 'bob', 'smith.com'),),
                                   (('Bob Smith', None, 'bob', 'smith.com'),),
                                   (('Bob Smith', None, 'bob', 'smith.com'),),
                                   (('Some One', None, 'some', 'one.com'), (None, None, 'foo', 'foo.com')),
                                   None, None, None, msg_id_header))

        def test_partial_fetch(self):
            self.client.append(self.base_folder, MULTIPART_MESSAGE)
            self.client.select_folder(self.base_folder)
            msg_id = self.client.search()[0]

            resp = self.client.fetch(msg_id, ['BODY[]<0.20>'])
            body = resp[msg_id]['BODY[]<0>']
            self.assertEqual(len(body), 20)
            self.assertTrue(body.startswith('From: Bob Smith'))

            resp = self.client.fetch(msg_id, ['BODY[]<2.25>'])
            body = resp[msg_id]['BODY[]<2>']
            self.assertEqual(len(body), 25)
            self.assertTrue(body.startswith('om: Bob Smith'))

        def test_fetch_modifiers(self):
            # CONDSTORE (RFC 4551) provides a good way to use FETCH
            # modifiers but it isn't commonly available.
            if not self.client.has_capability('CONDSTORE'):
                return self.skipTest("Server doesn't support CONDSTORE")

            # A little dance to ensure MODSEQ tracking is turned on - I'm looking at you Dovecot!
            self.client.select_folder(self.base_folder)
            self.client.append(self.base_folder, SIMPLE_MESSAGE)
            msg_id = self.client.search()[0]
            self.client.fetch(msg_id, ["MODSEQ"])
            self.client.close_folder()
            self.clear_folder(self.base_folder)

            # Actual testing starts here
            maxModSeq = int(self.client.select_folder(self.base_folder)['HIGHESTMODSEQ'][0])
            self.client.append(self.base_folder, SIMPLE_MESSAGE)
            msg_id = self.client.search()[0]
            resp = self.client.fetch(msg_id, ['FLAGS'], ['CHANGEDSINCE %d' % maxModSeq])
            self.assertIn('MODSEQ', resp[msg_id])

            # Prove that the modifier is actually being used
            resp = self.client.fetch(msg_id, ['FLAGS'], ['CHANGEDSINCE %d' % (maxModSeq + 1)])
            self.assertFalse(resp)

        def test_BODYSTRUCTURE(self):
            self.client.select_folder(self.base_folder)
            self.client.append(self.base_folder, SIMPLE_MESSAGE)
            self.client.append(self.base_folder, MULTIPART_MESSAGE)
            msgs = self.client.search()

            fetched = self.client.fetch(msgs, ['BODY', 'BODYSTRUCTURE'])

            # The expected test data is the same for BODY and BODYSTRUCTURE
            # since we can't predicate what the server we're testing against
            # will return.

            expected = ('text', 'plain', ('charset', 'us-ascii'), None, None, '7bit', 5, 1)
            self.check_BODYSTRUCTURE(expected, fetched[msgs[0]]['BODY'], multipart=False)
            self.check_BODYSTRUCTURE(expected, fetched[msgs[0]]['BODYSTRUCTURE'], multipart=False)

            expected = ([('text', 'html', ('charset', 'us-ascii'), None, None, 'quoted-printable', 55, 3),
                         ('text', 'plain', ('charset', 'us-ascii'), None, None, '7bit', 26, 1),
                         ],
                        'mixed',
                        ('boundary', '===============1534046211=='))
            self.check_BODYSTRUCTURE(expected, fetched[msgs[1]]['BODY'], multipart=True)
            self.check_BODYSTRUCTURE(expected, fetched[msgs[1]]['BODYSTRUCTURE'], multipart=True)

        def check_BODYSTRUCTURE(self, expected, actual, multipart=None):
            if multipart is not None:
                self.assertEqual(actual.is_multipart, multipart)

            # BODYSTRUCTURE lengths can various according to the server so
            # compare up until what is returned
            for e, a in zip(expected, actual):
                if have_matching_types(e, a, (list, tuple)):
                    for expected_and_actual in zip(e, a):
                        self.check_BODYSTRUCTURE(*expected_and_actual)
                else:
                    if e == ('charset', 'us-ascii') and a is None:
                        pass  # Some servers (eg. Gmail) don't return a charset when it's us-ascii
                    else:
                        a = lower_if_str(a)
                        e = lower_if_str(e)
                        self.assertEqual(a, e)

        def test_idle(self):
            if not self.client.has_capability('IDLE'):
                return self.skipTest("Server doesn't support IDLE")

            # Start main connection idling
            self.client.select_folder(self.base_folder)
            self.client.idle()

            # Start a new connection and upload a new message
            client2 = create_client_from_config(conf)
            client2.select_folder(self.base_folder)
            client2.append(self.base_folder, SIMPLE_MESSAGE)

            # Check for the idle data
            responses = self.client.idle_check(timeout=5)
            text, more_responses = self.client.idle_done()
            self.assertIn((1, 'EXISTS'), responses)
            self.assertTrue(isinstance(text, str))
            self.assertGreater(len(text), 0)
            self.assertTrue(isinstance(more_responses, list))

            # Check for IDLE data returned by idle_done()
            self.client.idle()
            client2.select_folder(self.base_folder)
            client2.append(self.base_folder, SIMPLE_MESSAGE)
            time.sleep(2)    # Allow some time for the IDLE response to be sent

            text, responses = self.client.idle_done()
            self.assertIn((2, 'EXISTS'), responses)
            self.assertTrue(isinstance(text, str))
            self.assertGreater(len(text), 0)

        def test_noop(self):
            self.client.select_folder(self.base_folder)

            # Initially there should be no responses
            text, resps = self.client.noop()
            self.assertTrue(isinstance(text, str))
            self.assertGreater(len(text), 0)
            self.assertEquals(resps, [])

            # Start a new connection and upload a new message
            client2 = create_client_from_config(conf)
            client2.select_folder(self.base_folder)
            client2.append(self.base_folder, SIMPLE_MESSAGE)

            # Check for this addition in the NOOP data
            msg, resps = self.client.noop()
            self.assertTrue(isinstance(text, str))
            self.assertGreater(len(text), 0)
            self.assertTrue(isinstance(resps, list))
            self.assertIn((1, 'EXISTS'), resps)

        def test_expunge(self):
            self.client.select_folder(self.base_folder)

            # Test empty mailbox
            text, resps = self.client.expunge()
            self.assertTrue(isinstance(text, str))
            self.assertGreater(len(text), 0)
            # Some servers return nothing while others (e.g. Exchange) return (0, 'EXISTS')
            self.assertIn(resps, ([], [(0, 'EXISTS')]))

            # Now try with a message to expunge
            self.client.append(self.base_folder, SIMPLE_MESSAGE, flags=[imapclient.DELETED])

            msg, resps = self.client.expunge()

            self.assertTrue(isinstance(text, str))
            self.assertGreater(len(text), 0)
            self.assertTrue(isinstance(resps, list))
            if not self.is_gmail():
                # GMail has an auto-expunge feature which might be
                # on. EXPUNGE won't return anything in this case
                self.assertIn((1, 'EXPUNGE'), resps)

        def test_getacl(self):
            self.skip_unless_capable('ACL')

            folder = self.add_prefix_to_folder('test_acl')
            who = conf['username']
            self.client.create_folder(folder)

            rights = self.client.getacl(folder)
            self.assertIn(who, [u for u, r in rights])

    return LiveTest


def lower_if_str(val):
    if isinstance(val, basestring):
        return val.lower()
    return val

def have_matching_types(a, b, type_or_types):
    """True if a and b are instances of the same type and that type is
    one of type_or_types.
    """
    if not isinstance(a, type_or_types):
        return False
    return isinstance(b, type(a))

def argv_error(msg):
    print >> sys.stderr, msg
    print >> sys.stderr
    print >> sys.stderr, "usage: %s <livetest.ini> [ optional unittest arguments ]" % sys.argv[0]
    sys.exit(1)

def parse_argv():
    args = sys.argv[1:]
    if not args:
        argv_error('Please specify a host configuration file. See livetest-sample.ini for an example.')
    ini_path = sys.argv.pop(1)  # 2nd arg should be the INI file
    if not os.path.isfile(ini_path):
        argv_error('%r is not a livetest INI file' % ini_path)
    host_config = parse_config_file(ini_path)
    return host_config

def probe_host(config):
    client = create_client_from_config(config)
    ns = client.namespace()
    client.logout()
    if not ns.personal:
        raise RuntimeError('Can\'t run tests: IMAP account has no personal namespace')
    return ns.personal[0]   # Use first personal namespace

def main():
    host_config = parse_argv()

    namespace = probe_host(host_config)
    host_config.namespace = namespace

    live_test_mod = imp.new_module('livetests')
    sys.modules['livetests'] = live_test_mod

    def add_test_class(name, klass):
       klass.__name__ = name
       setattr(live_test_mod, name, klass)

    add_test_class('TestWithUIDs', createLiveTestClass(host_config, use_uid=True))
    add_test_class('TestWithoutUIDs', createLiveTestClass(host_config, use_uid=False))

    unittest.main(module='livetests')

if __name__ == '__main__':
    main()
