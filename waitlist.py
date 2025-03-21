import pickle
import random
import string
import os

class Waitlist:
    def __init__(self, filename='waitlist.pkl'):
        self.filename = filename
        self.waitlist = self.load_from_pickle()

    def generate_id(self, length=12):
        """Generate a unique 12-character ID."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def save_to_pickle(self):
        """Save the waitlist to a pickle file."""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.waitlist, f)

    def load_from_pickle(self):
        """Load the waitlist from a pickle file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    def create_ad(self,inner_data):
        """Create a new ad and add it to the waitlist."""
        self.waitlist = self.load_from_pickle()  # Reload waitlist
        entry_id = self.generate_id()
        self.waitlist[entry_id] = inner_data
        self.save_to_pickle()  # Save changes
        return entry_id

    def remove_ad(self, entry_id):
        """Remove an ad from the waitlist using its ID."""
        self.waitlist = self.load_from_pickle()  # Reload waitlist
        if entry_id in self.waitlist:
            del self.waitlist[entry_id]
            self.save_to_pickle()  # Save changes
        else:
            print("ID not found in waitlist.")

    def get_ad(self, entry_id):
        """Get the data of an ad by its ID."""
        self.waitlist = self.load_from_pickle()  # Reload waitlist
        return self.waitlist.get(entry_id, "ID not found in waitlist.")

