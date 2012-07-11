# Copyright 2012 10gen, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from logl.filters.stale_secondary import *
from datetime import datetime


def test_criteria():
    """Test the criteria() method of stale_secondary.py"""
    assert criteria("this should not pass") == -1
    assert criteria("Thu Sep 9 17:22:46 [rs_sync] replSet error RS102 too stale to catch up") == 0
    assert criteria("Thu Sep 9 17:24:46 [rs_sync] replSet error RS102 too stale to catch up, at least from primary: 127.0.0.1:30000") == 0


def test_process():
    """Test the process() method of stale_secondary.py"""
    date = datetime.now()
    check_state("Thu Sep 9 17:22:46 [rs_sync] replSet error RS102 too stale to catch up", 0, date, None)
    check_state("Thu Sep 9 17:24:46 [rs_sync] replSet error RS102 too stale to catch up, at least from primary: 127.0.0.1:30000", 0, date, "127.0.0.1:30000")
    check_state("Thu Sep 9 17:24:46 [rs_sync] replSet error RS102 too stale to catch up, at least from primary: sam@10gen.com:27017", 0, date, "sam@10gen.com:27017")
    assert process("This should fail", date) == None


def check_state(message, code, date, server):
    """Helper method for tests"""
    doc = process(message, date)
    assert doc
    assert doc["type"] == "stale"
    assert doc["original_message"] == message
    if server != None:
        assert doc["info"]["server"] == server
