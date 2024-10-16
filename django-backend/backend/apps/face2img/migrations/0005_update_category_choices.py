from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('face2img', '0004_pack_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='category',
            field=models.CharField(
                choices=[
                    ('LinkedIn', 'LinkedIn'),
                    ('Hair style', 'Hair style'),
                    ('Smart tool', 'Smart tool'),
                    ('Travel', 'Travel'),
                    ('Classy', 'Classy'),
                    ('Fashion', 'Fashion'),
                    ('Decades transformations', 'Decades transformations'),
                    ('Movies', 'Movies'),
                    ('Y2K', 'Y2K'),
                    ('Activities', 'Activities'),
                    ('Suit', 'Suit'),
                    ('Office', 'Office'),
                    ('Casual', 'Casual'),
                    ('Business', 'Business'),
                    ('Black background', 'Black background'),
                    ('White background', 'White background'),
                    ('Casual selfie', 'Casual selfie'),
                    ('Bob cut', 'Bob cut'),
                    ('Colorful hair', 'Colorful hair'),
                    ('Brown hair', 'Brown hair'),
                    ('Buzz cut', 'Buzz cut'),
                    ('Curly', 'Curly'),
                    ('Ginger', 'Ginger'),
                    ('Old money', 'Old money'),
                    ('Beach', 'Beach'),
                    ('Blond', 'Blond'),
                    ('Santorini', 'Santorini'),
                    ('Eiffel Tower', 'Eiffel Tower'),
                    ('Bora bora', 'Bora bora'),
                    ('Grand Canyon', 'Grand Canyon'),
                    ('Cappadocia', 'Cappadocia'),
                    ('Niagara Falls', 'Niagara Falls'),
                    ('Istanbul', 'Istanbul'),
                    ('Clinique yerde', 'Clinique yerde'),
                    ('Tak mahal', 'Tak mahal'),
                    ('Colesseum', 'Colesseum'),
                    ('Monaco', 'Monaco'),
                    ('Venice', 'Venice'),
                    ('Maldives', 'Maldives'),
                    ('Sydney', 'Sydney'),
                    ('Hong Kong', 'Hong Kong'),
                    ('Japan', 'Japan'),
                    ('Dubai', 'Dubai'),
                    ('Milan', 'Milan'),
                    ('Switzerland', 'Switzerland'),
                    ('Munich', 'Munich'),
                    ('Luxury', 'Luxury'),
                    ('Date', 'Date'),
                    ('Coffee date', 'Coffee date'),
                    ('Wedding', 'Wedding'),
                    ('Red carpet', 'Red carpet'),
                    ('Elite', 'Elite'),
                    ('Yacht', 'Yacht'),
                    ('Private jet', 'Private jet'),
                    ('Opera', 'Opera'),
                    ('Podium', 'Podium'),
                    ('Studio shooting', 'Studio shooting'),
                    ('Street style', 'Street style'),
                    ('Look book', 'Look book'),
                    ('Black & white', 'Black & white'),
                    ('The 1940s', 'The 1940s'),
                    ('The 1950s', 'The 1950s'),
                    ('The 1960s', 'The 1960s'),
                    ('The 1970s', 'The 1970s'),
                    ('The 1980s arcade', 'The 1980s arcade'),
                    ('The 1980s', 'The 1980s'),
                    ('The 1990s', 'The 1990s'),
                    ('The 2000s', 'The 2000s'),
                    ('Monochrome Polaroid', 'Monochrome Polaroid'),
                    ('Polaroid', 'Polaroid'),
                    ('The walking dead', 'The walking dead'),
                    ('The hunger games', 'The hunger games'),
                    ('Avatar', 'Avatar'),
                    ('Marvel', 'Marvel'),
                    ('Suicide Squad', 'Suicide Squad'),
                    ('Game of Thrones', 'Game of Thrones'),
                    ('Breaking bad', 'Breaking bad'),
                    ('Friends', 'Friends'),
                    ('Desperate housewives', 'Desperate housewives'),
                    ('The last of us', 'The last of us'),
                    ('Yves Saint Laurent', 'Yves Saint Laurent'),
                    ('Burberry', 'Burberry'),
                    ('Dior', 'Dior'),
                    ('Prada', 'Prada'),
                    ('Chanel', 'Chanel'),
                    ('Hermes', 'Hermes'),
                    ('Louis Vuitton', 'Louis Vuitton'),
                    ('Chloe', 'Chloe'),
                    ('Athlete', 'Athlete'),
                    ('Goth', 'Goth'),
                    ('Nerd', 'Nerd'),
                    ('Prom skater', 'Prom skater'),
                    ('Hip hop', 'Hip hop'),
                    ('Horse riding', 'Horse riding'),
                    ('Tennis', 'Tennis'),
                    ('Golf', 'Golf'),
                ],
                default='Smart tool',
                max_length=255,
                verbose_name='Category'
            ),
        ),
    ]
