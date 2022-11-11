#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime, date
from models import Artist, Venue, Shows
from config import db, SQLALCHEMY_DATABASE_URI

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


app = Flask(__name__)  # initialise flask app
moment = Moment(app)
# load all config values into app.config dictionary
app.config.from_object('config')
db.init_app(app)  # link to sqlalchemy database api

# connect to a local postgresql database
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@ app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@ app.route('/venues')
def venues():

    data = []
    places = Venue.query.distinct(Venue.city, Venue.state)
    for place in places:  # iterate over each state
        # get filtered table of venues in state
        state_venues = Venue.query.filter_by(
            state=place.state).distinct().all()
        state_venues_list = []
        # for each venue in the state venues, pull relevant data
        for venue in state_venues:
            num_upcoming_shows = Shows.query.filter_by(
                venue_id=venue.id).count()
            venues = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": num_upcoming_shows
            }
            # append all venue dictionaries to fill the list
            state_venues_list.append(venues)
        # append all data
        data.append({
            "city": place.city,
            "state": place.state,
            "venues": state_venues_list
        })

    return render_template('pages/venues.html', areas=data)


@ app.route('/venues/search', methods=['POST'])
def search_venues():
    # case insensitive search
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
    data = []
    # iterate over filtered venues and add properties to data list
    for venue in venues:
        num_upcoming_shows = Shows.query.filter(
            Shows.venue_id == venue.id).count()
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
        })
    response = {
        "count": len(data),
        "data": data
    }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@ app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get(venue_id)
    # join Shows and Artist table, filter Shows table on venue id
    shows_artist = Shows.query.join(Artist).filter(
        Shows.venue_id == venue_id)
    # calculate and format todays date to split shows into past/future
    today = datetime.now()
    today = date(today.year, today.month, today.day)
    past_shows, upcoming_shows = [], []
    # separate data by date
    for show_artist in shows_artist:
        if show_artist.start_time < today:
            past_shows.append({
                "artist_id": show_artist.artist.id,
                "artist_name": show_artist.artist.name,
                "artist_image_link": show_artist.artist.image_link,
                "start_time": str(show_artist.start_time)
            })
        else:
            upcoming_shows.append({
                "artist_id": show_artist.artist.id,
                "artist_name": show_artist.artist.name,
                "artist_image_link": show_artist.artist.image_link,
                "start_time": str(show_artist.start_time)
            })

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres if venue.genres else ['TBC'],
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
        # create new venue, add to database and commit
        venue = Venue(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            genres=request.form.getlist('genres'),  # use getlist for an array
            website=request.form.get('website_link'),
            seeking_talent=True if request.form.get(
                'seeking_talent') == 'y' else False,
            seeking_description=request.form.get('seeking_description')
        )
        db.session.add(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            # on unsuccessful db insert, flash an error
            flash('An error occurred. Venue ' +
                  request.form.get('name') + ' could not be listed.')
        else:
            # on successful db insert, flash success
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')

    return render_template('pages/home.html')


@ app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # Delete a record. Handle cases where the session commit could fail.
    error = False
    try:
        Venue.query.get(venue_id).delete()
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            # flash error
            flash('Venue ' + venue_id + ' could not be deleted.')
        else:
            # flash success
            flash('Venue ' + venue_id + ' was deleted successfully.')

    return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------


@ app.route('/artists')
def artists():
    # show all artist id and names
    data = []
    artists = Artist.query.all()
    for artist in artists:
        data.append(
            {
                "id": artist.id,
                "name": artist.name
            }
        )

    return render_template('pages/artists.html', artists=data)


@ app.route('/artists/search', methods=['POST'])
def search_artists():
    # case insensitive search
    search_term = request.form.get('search_term')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
    data = []
    today = datetime.now()
    # iterate over all artists and append data
    for artist in artists:
        filter_criteria = [Shows.artist_id == artist.id,
                           Shows.start_time > today]
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": Shows.query.filter(*filter_criteria).count()
        })

    response = {
        "count": artists.count(),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    artist = Artist.query.get(artist_id)
    # join shows and venue tables, filter by artist id
    shows_venues = Shows.query.join(Venue).filter(
        Shows.artist_id == artist_id)
    # calculate and format todays date to split shows into past/future
    today = datetime.now()
    today = date(today.year, today.month, today.day)
    past_shows, upcoming_shows = [], []
    # split shows by time
    for show_venue in shows_venues:
        if show_venue.start_time < today:
            past_shows.append({
                "venue_id": show_venue.venue.id,
                "venue_name": show_venue.venue.name,
                "venue_image_link": show_venue.venue.image_link,
                "start_time": str(show_venue.start_time)
            })
        else:
            upcoming_shows.append({
                "venue_id": show_venue.venue.id,
                "venue_name": show_venue.venue.name,
                "venue_image_link": show_venue.venue.image_link,
                "start_time": str(show_venue.start_time)
            })

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "address": artist.address,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    # get and return artist data
    artist = Artist.query.get(artist_id)
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link
    }

    return render_template('forms/edit_artist.html', form=form, artist=data)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form.get('name')
        artist.genres = request.form.getlist('genres')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.website = request.form.get('website_link')
        artist.facebook_link = request.form.get('facebook_link')
        artist.seeking_venue = True if request.form.get(
            'seeking_venue') == 'y' else False
        artist.seeking_description = request.form.get('seeking_description')
        artist.image_link = request.form.get('image_link')
        db.session.commit()
    except Exception:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # get and return venue data
    venue = Venue.query.get(venue_id)
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link
    }

    return render_template('forms/edit_venue.html', form=form, venue=data)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # venue record with ID <venue_id> using the new attributes
    try:
        venue = Venue.query.get(venue_id)
        venue.name = request.form.get('name')
        venue.genres = request.form.getlist('genres')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.phone = request.form.get('phone')
        venue.website = request.form.get('website_link')
        venue.facebook_link = request.form.get('facebook_link')
        venue.seeking_talent = True if request.form.get(
            'seeking_talent') == 'y' else False
        venue.seeking_description = request.form.get('seeking_description')
        venue.image_link = request.form.get('image_link')
        db.session.commit()
    except Exception:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    error = False
    try:
        # get request data, add and commit to database
        artist = Artist(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            genres=request.form.getlist('genres'),  # use getlist for an array
            website=request.form.get('website_link'),
            seeking_venue=True if request.form.get(
                'seeking_venue') == 'y' else False,
            seeking_description=request.form.get('seeking_description'),
            image_link=request.form.get('image_link'),
            facebook_link=request.form.get('facebook_link')
        )
        db.session.add(artist)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            # on unsuccessful db insert, flash an error
            flash('An error occurred. Artist ' +
                  request.form.get('name') + ' could not be listed.')
        else:
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    # displays list of shows at /shows
    all_shows = Shows.query.join(Artist).join(Venue)
    data = []
    for show in all_shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        })

    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    error = False
    try:
        show = Shows(
            artist_id=request.form.get('artist_id'),
            venue_id=request.form.get('venue_id'),
            start_time=request.form.get('start_time')
        )
        db.session.add(show)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            # on unsuccessful db insert, flash an error
            flash('An error occurred. Show could not be listed.')
        else:
            # on successful db insert, flash success
            flash('Show was successfully listed!')
    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
