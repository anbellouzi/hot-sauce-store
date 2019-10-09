from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_item_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_item = {
    'title': 'Peperica',
    'description': 'Very spicy',
    'img': 'https://youtube.com/embed/hY7m5jjJ9mM',
    'price': 20,
    'created_at': 'October 9th 2019'

}
sample_form_data = {
    'title': sample_item['title'],
    'description': sample_item['description'],
    'img': sample_item['img'],
    'price': sample_item['price'],
    'created_at': sample_item['created_at']

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

    # @mock.patch('pymongo.collection.Collection.find_one')
    # def test_edit_item(self, mock_find):
    #     """Test editing a single item."""
    #     mock_find.return_value = sample_item
    #
    #     result = self.client.get(f'/items/{sample_item_id}/edit')
    #     self.assertEqual(result.status, '200 OK')
    #     self.assertIn(b'Peperica', result.data)

    # @mock.patch('pymongo.collection.Collection.insert_one')
    # def test_submit_playlist(self, mock_insert):
    #     """Test submitting a new item."""
    #     result = self.client.post('/items', data=sample_form_data)
    #
    #     # After submitting, should redirect to that playlist's page
    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_insert.assert_called_with(sample_item)


if __name__ == '__main__':
    unittest_main()
