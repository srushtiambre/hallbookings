# College Hall Booking System

A Django-based web application for managing college hall bookings with an improved, modern user interface.

## Features

- **4 College Halls**: Manage bookings for Auditorium A, Conference Hall B, Seminar Room C, and Banquet Hall D
- **User Authentication**: Secure login system for students and staff
- **Hall Details**: View capacity, location, amenities, and availability of each hall
- **Booking Management**: Submit, view, and cancel booking requests
- **Admin Interface**: Django admin panel for approving/rejecting bookings
- **Real-time Availability**: Check hall availability using AJAX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations

## Tech Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite3
- **Python**: 3.8+

## Project Structure

```
hallbooking/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database
├── init_db.py              # Database initialization script
│
├── hallbooking/            # Main Django project
│   ├── settings.py         # Project settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── __init__.py
│
├── bookings/               # Django app for hall bookings
│   ├── models.py          # Hall, Booking models
│   ├── views.py           # View functions
│   ├── urls.py            # App URLs
│   ├── admin.py           # Admin configuration
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/        # Database migrations
│   └── templates/bookings/
│       ├── index.html             # Home page
│       ├── hall_detail.html       # Hall details
│       ├── book_hall.html         # Booking form
│       ├── booking_confirmation.html
│       ├── my_bookings.html       # User's bookings
│       └── login.html             # Login page
│
├── templates/
│   └── base.html           # Base template
│
└── static/
    ├── css/
    │   └── style.css       # Main stylesheet
    └── js/
        └── main.js         # JavaScript functions
```

## Installation & Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Apply Database Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

When prompted:
- Username: `admin`
- Email: `admin@college.edu`
- Password: (enter your preferred password)

### 4. Initialize Sample Halls

```bash
python init_db.py
```

This will create the 4 college halls in the database:
- Auditorium A (500 capacity)
- Conference Hall B (300 capacity)
- Seminar Room C (100 capacity)
- Banquet Hall D (200 capacity)

## Running the Application

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000/`

### Admin Panel

Access the Django admin panel at: `http://localhost:8000/admin/`

Use your superuser credentials to:
- Manage halls
- View and approve/reject booking requests
- Manage users
- Configure amenities and availability

## Usage

### For Students/Users

1. **View Halls**: Browse available halls on the homepage
2. **Hall Details**: Click on a hall to see details, amenities, and upcoming bookings
3. **Book a Hall**: 
   - Click "Book Now" button
   - Fill in event details (purpose, attendees)
   - Select date and time
   - Submit the booking request
4. **Track Bookings**: View all your bookings in "My Bookings"
5. **Cancel Booking**: Cancel pending or approved bookings if needed

### For Administrators

1. **Approve Bookings**: Review pending requests in admin panel
2. **Reject with Reason**: Reject requests with a custom reason
3. **Manage Halls**: Add, edit, or remove halls
4. **View Analytics**: See booking statistics and trends

## Database Models

### Hall Model
- `name`: Hall name (e.g., "Auditorium A")
- `capacity`: Maximum occupancy
- `location`: Physical location
- `description`: Detailed description
- `amenities`: List of available amenities
- `available`: Availability status
- `created_at`: Creation timestamp

### Booking Model
- `hall`: Foreign key to Hall
- `user`: Foreign key to User
- `booking_date`: Event date
- `start_time`: Event start time
- `end_time`: Event end time
- `purpose`: Event purpose
- `expected_attendees`: Number of attendees
- `status`: Booking status (pending, approved, rejected, cancelled)
- `approved_by`: Staff member who approved
- `rejection_reason`: Reason for rejection if applicable

## Key Features Explained

### Availability Checking
The system prevents double bookings by:
- Checking existing bookings for the same hall on the selected date
- Validating time slots don't overlap
- Performing AJAX real-time availability checks

### Validation
Booking validation includes:
- Future dates only
- Expected attendees ≤ hall capacity
- Start time before end time
- No conflicting bookings

### User Authentication
- Django's built-in authentication system
- Secure password handling
- Login required for bookings
- User-specific booking history

## Customization

### Adding More Halls
Edit `init_db.py` to add additional halls, then run:
```bash
python init_db.py
```

### Styling
Modify `static/css/style.css` to customize colors, fonts, and layout

### Adding Features
- Add fields to models in `bookings/models.py`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`

## Settings Reference

Key settings in `hallbooking/settings.py`:
- `DEBUG = True` (Change to False in production)
- `ALLOWED_HOSTS = ['*']` (Restrict in production)
- `SECRET_KEY` (Change in production)
- `TIME_ZONE = 'UTC'` (Modify for your location)

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Errors
Reset the database (WARNING: loses all data):
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python init_db.py
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

## Future Enhancements

- Email notifications for booking status
- Payment integration
- Advanced booking calendar
- User profile management
- Booking recurrence options
- Equipment/catering add-ons
- Feedback and ratings system
- Multi-language support

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
1. Check the admin panel for booking status
2. Contact the college administration
3. Review logs at the server console

---

**Developed for College Hall Management System**
