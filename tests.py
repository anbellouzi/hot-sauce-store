from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app
from datetime import datetime

sample_item_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_item = {
    'title': 'Peperica',
    'description': 'Very spicy',
    'price': '20',
    'img': 'https://youtube.com/embed/hY7m5jjJ9mM',
}

sample_form_data = {
    'title': sample_item['title'],
    'description': sample_item['description'],
    'images': sample_item['img'],
    'price': sample_item['price'],

}

class PlaylistsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the playlists homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Item', result.data)

    def test_new(self):
        """Test the new playlist creation page."""
        result = self.client.get('/item/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Item', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_item(self, mock_find):
        """Test showing a single item."""
        mock_find.return_value = sample_item

        result = self.client.get(f'/shop/item/{sample_item_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Peperica', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_item(self, mock_find):
        """Test editing a single item."""
        mock_find.return_value = sample_item

        result = self.client.get(f'/items/{sample_item_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Peperica', result.data)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_playlist(self, mock_update):
        result = self.client.post(f'/item/{sample_item_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_item_id}, {'$set': sample_item})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_item(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/items/{sample_item_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_item_id})

if __name__ == '__main__':
    unittest_main()
