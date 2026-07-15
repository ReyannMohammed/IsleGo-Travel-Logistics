# Database Schema (Proposed)

This document explains the database design for the IsleGo booking platform. The current prototype implements `Client` and `Booking` tables. Below is a recommended expanded schema for production-ready functionality.

## Current tables (prototype)

- Clients
  - `id` (PK)
  - `name`
  - `email`
  - `phone`
  - `company`

- Bookings
  - `id` (PK)
  - `booking_code` (unique)
  - `destination`
  - `travel_date`
  - `status`
  - `notes`
  - `created_at`
  - `client_id` (FK -> Clients.id)

## Recommended additional tables

- Users (staff)
  - `id`, `username`, `email`, `role` (admin, coordinator), `password_hash`

- Itineraries
  - `id`, `booking_id` (FK), `title`, `start_date`, `end_date`, `details`

- ItineraryItems (tasks/events)
  - `id`, `itinerary_id` (FK), `type` (flight/hotel/tour), `start_time`, `end_time`, `status`, `vendor_id`

- Vendors
  - `id`, `name`, `service_type`, `contact_email`, `phone`

- Payments
  - `id`, `booking_id` (FK), `amount`, `currency`, `status`, `paid_at`

## Relationships
- One `Client` can have many `Booking` entries.
- One `Booking` has one `Itinerary` (or many itineraries depending on design).
- `Itinerary` contains many `ItineraryItems` which may reference `Vendors`.
- `Users` manage `Bookings` and `Itineraries` (via auditing fields).

## Indexes & Performance
- Index `booking_code` and `travel_date` for faster lookups.
- Consider partial indexes for `status = 'Pending'` queries.

## Security & Privacy Notes
- Store PII securely and encrypt sensitive fields when storing passport or payment data.
- Use hashed passwords and role-based access control for staff accounts.

## Example SQL (Create core tables)

```sql
CREATE TABLE clients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  company TEXT
);

CREATE TABLE bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  booking_code TEXT UNIQUE NOT NULL,
  destination TEXT NOT NULL,
  travel_date DATE NOT NULL,
  status TEXT DEFAULT 'Pending',
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  client_id INTEGER NOT NULL,
  FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);
```
