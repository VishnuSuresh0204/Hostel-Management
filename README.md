# Hostel Management System

A premium Student Co-Living management platform built with Django and Bootstrap 5. Designed for elite hostels across Kerala's education hubs, this system provides a seamless experience for administrators, permanent residents, and short-term guests.

## 🚀 Features

### For Administrators
- **Room Management**: Add, edit, and track room status/capacity.
- **Member Management**: View and manage residents and guests; block/unblock accounts.
- **Fee Management**: Assign and track room and mess fees.
- **Mess & Events**: Coordinate daily menus and schedule student events.
- **Bookings & Requests**: Approve/Reject room bookings and leave requests.

### For Residents (Students)
- **Room Booking**: Real-time availability with a minimum 20-day stay requirement.
- **Financials**: View and track pending/paid fees.
- **Daily Living**: Access daily mess menus and upcoming events.
- **Requests**: Submit leave requests and feedback directly to administration.

### For Guests
- **Short-term Stays**: Quick booking system with a maximum 7-day stay limit.
- **Simple Experience**: Easy feedback submission and booking tracking.

### Secure Payments
- Integrated payment portal with real-time card validation for secure transactions.

## 🛠️ Technology Stack
- **Backend**: Django (Python)
- **Frontend**: Bootstrap 5, Vanilla JavaScript, CSS3
- **Database**: SQLite (Development)
- **Icons**: FontAwesome 5

## 🔧 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VishnuSuresh0204/Hostel-Management.git
   cd Hostel-Management
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django
   ```

4. **Run migrations**:
   ```bash
   python hostel/manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python hostel/manage.py runserver
   ```

## 🔒 Form Validations
The project features a centralized validation architecture:
- **Strong Auth**: Pattern-matched usernames and passwords.
- **Date Constraints**: Dynamic min/max stay logic for residents vs guests.
- **Payment Security**: Strict 16-digit card and MM/YY expiry validation.

## 📄 License
This project is licensed under the MIT License.
