import unittest
from models.legislative import Parliament, Parliamentarian, Chamber, ParliamentaryStatus

class TestParliament(unittest.TestCase):
    def setUp(self):
        self.parliament = Parliament(300)

    def test_parliament_quorum(self):
        # Fill the parliament with active members
        for _ in range(300):
            member = Parliamentarian(None, Chamber.DEPUTIES)
            member.status = ParliamentaryStatus.ACTIVE
            self.parliament.add_member(member)

        # Check if the parliament has a quorum
        self.assertTrue(self.parliament.has_quorum())

        # Remove members until quorum is lost
        members_to_remove = int(300 * 0.51)  # Remove just over 50% of members
        for _ in range(members_to_remove):
            member = self.parliament.members[-1]  # Get the last member without removing
            self.parliament.remove_member(member)

        # Check that quorum is lost
        self.assertFalse(self.parliament.has_quorum())

if __name__ == '__main__':
    unittest.main()
