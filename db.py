import pickle
import random
import string
import os

class AdDatabase:
    def __init__(self, filename='database.pkl'):
        self.filename = filename
        self.database = self.load_from_pickle()

    def generate_id(self, length=12):
        """Generate a unique 12-character ID."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def save_to_pickle(self):
        """Save the database to a pickle file."""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.database, f)

    def load_from_pickle(self):
        """Load the database from a pickle file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    def add_ad(self,inner_data):
        """Add a new ad to the database."""
        self.database = self.load_from_pickle()  # Reload database
        entry_id = self.generate_id()
        self.database[entry_id] = inner_data
        self.save_to_pickle()  # Save changes
        return entry_id

    def delete_ad(self, entry_id):
        """Delete an ad from the database using its ID."""
        self.database = self.load_from_pickle()  # Reload database
        if entry_id in self.database:
            del self.database[entry_id]
            self.save_to_pickle()  # Save changes
        else:
            print("ID not found in database.")

    def search_ad(self, keywords):
        self.database = self.load_from_pickle()  # Reload database
        matching_ads = {}
        for entry_id, ad in self.database.items():
            if  any(keyword.lower() in ad['title'].lower() or keyword.lower() in ad['description'].lower() for keyword in keywords):
                matching_ads[entry_id] = ad

        return matching_ads

    def get_ad_by_id(self, entry_id):
        """Get the data of an ad by its ID."""
        self.database = self.load_from_pickle()  # Reload database
        return self.database.get(entry_id, None)


