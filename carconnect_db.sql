-- Create the database
CREATE DATABASE IF NOT EXISTS CarConnect;
USE CarConnect;

-- Create Customer table
CREATE TABLE IF NOT EXISTS Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    PhoneNumber VARCHAR(15) NOT NULL,
    Address TEXT NOT NULL,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(100) NOT NULL,
    RegistrationDate DATE NOT NULL
);

-- Create Vehicle table
CREATE TABLE IF NOT EXISTS Vehicle (
    VehicleID INT AUTO_INCREMENT PRIMARY KEY,
    Model VARCHAR(50) NOT NULL,
    Make VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    Color VARCHAR(30) NOT NULL,
    RegistrationNumber VARCHAR(20) NOT NULL UNIQUE,
    Availability BOOLEAN NOT NULL DEFAULT TRUE,
    DailyRate DECIMAL(10, 2) NOT NULL
);

-- Create Reservation table
CREATE TABLE IF NOT EXISTS Reservation (
    ReservationID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    VehicleID INT NOT NULL,
    StartDate DATETIME NOT NULL,
    EndDate DATETIME NOT NULL,
    TotalCost DECIMAL(10, 2) NOT NULL,
    Status VARCHAR(20) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID)
);

-- Create Admin table
CREATE TABLE IF NOT EXISTS Admin (
    AdminID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    PhoneNumber VARCHAR(15) NOT NULL,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(100) NOT NULL,
    Role VARCHAR(50) NOT NULL,
    JoinDate DATE NOT NULL
);

-- Insert sample customers
INSERT INTO Customer (FirstName, LastName, Email, PhoneNumber, Address, Username, Password, RegistrationDate) VALUES
('John', 'Doe', 'john.doe@example.com', '555-0101', '123 Main St, Anytown', 'johndoe', 'password123', '2023-01-15'),
('Jane', 'Smith', 'jane.smith@example.com', '555-0102', '456 Oak Ave, Somewhere', 'janesmith', 'securepass', '2023-02-20'),
('Robert', 'Johnson', 'robert.j@example.com', '555-0103', '789 Pine Rd, Nowhere', 'robjohn', 'myp@ssword', '2023-03-10'),
('Emily', 'Williams', 'emily.w@example.com', '555-0104', '321 Elm St, Anycity', 'emilyw', 'emilypass', '2023-04-05'),
('Michael', 'Brown', 'michael.b@example.com', '555-0105', '654 Maple Dr, Yourtown', 'mikebrown', 'brownie123', '2023-05-12'),
('Sarah', 'Davis', 'sarah.d@example.com', '555-0106', '987 Cedar Ln, Thistown', 'sarahd', 'davis456', '2023-06-18'),
('David', 'Miller', 'david.m@example.com', '555-0107', '135 Birch Blvd, Thatcity', 'davidm', 'millertime', '2023-07-22'),
('Jessica', 'Wilson', 'jessica.w@example.com', '555-0108', '246 Walnut Way, Otherville', 'jessw', 'wilson789', '2023-08-30'),
('Thomas', 'Moore', 'thomas.m@example.com', '555-0109', '369 Spruce St, Newtown', 'tommoore', 'moorepass', '2023-09-14'),
('Jennifer', 'Taylor', 'jennifer.t@example.com', '555-0110', '159 Willow Ave, Oldcity', 'jennyt', 'taylor123', '2023-10-25');

-- Insert sample vehicles
INSERT INTO Vehicle (Model, Make, Year, Color, RegistrationNumber, Availability, DailyRate) VALUES
('Corolla', 'Toyota', 2022, 'Silver', 'TOY-1234', TRUE, 45.00),
('Civic', 'Honda', 2023, 'Red', 'HON-5678', TRUE, 50.00),
('Accord', 'Honda', 2021, 'Black', 'HON-9012', FALSE, 55.00),
('Camry', 'Toyota', 2023, 'Blue', 'TOY-3456', TRUE, 60.00),
('Altima', 'Nissan', 2022, 'White', 'NIS-7890', TRUE, 48.00),
('F-150', 'Ford', 2023, 'Black', 'FOR-1234', TRUE, 75.00),
('Silverado', 'Chevrolet', 2021, 'Gray', 'CHE-5678', FALSE, 70.00),
('Model 3', 'Tesla', 2023, 'Red', 'TES-9012', TRUE, 90.00),
('Rogue', 'Nissan', 2022, 'Silver', 'NIS-3456', TRUE, 52.00),
('Wrangler', 'Jeep', 2023, 'Green', 'JEE-7890', TRUE, 65.00);

-- Insert sample admins
INSERT INTO Admin (FirstName, LastName, Email, PhoneNumber, Username, Password, Role, JoinDate) VALUES
('Admin', 'One', 'admin1@carconnect.com', '555-1001', 'admin1', 'adminpass1', 'Super Admin', '2023-01-01'),
('Admin', 'Two', 'admin2@carconnect.com', '555-1002', 'admin2', 'adminpass2', 'Manager', '2023-01-15'),
('Admin', 'Three', 'admin3@carconnect.com', '555-1003', 'admin3', 'adminpass3', 'Support', '2023-02-01'),
('Admin', 'Four', 'admin4@carconnect.com', '555-1004', 'admin4', 'adminpass4', 'Fleet Manager', '2023-02-15'),
('Admin', 'Five', 'admin5@carconnect.com', '555-1005', 'admin5', 'adminpass5', 'Support', '2023-03-01'),
('Admin', 'Six', 'admin6@carconnect.com', '555-1006', 'admin6', 'adminpass6', 'Manager', '2023-03-15'),
('Admin', 'Seven', 'admin7@carconnect.com', '555-1007', 'admin7', 'adminpass7', 'Support', '2023-04-01'),
('Admin', 'Eight', 'admin8@carconnect.com', '555-1008', 'admin8', 'adminpass8', 'Fleet Manager', '2023-04-15'),
('Admin', 'Nine', 'admin9@carconnect.com', '555-1009', 'admin9', 'adminpass9', 'Support', '2023-05-01'),
('Admin', 'Ten', 'admin10@carconnect.com', '555-1010', 'admin10', 'adminpass10', 'Manager', '2023-05-15');

-- Insert sample reservations
INSERT INTO Reservation (CustomerID, VehicleID, StartDate, EndDate, TotalCost, Status) VALUES
(1, 1, '2023-11-01 09:00:00', '2023-11-03 17:00:00', 90.00, 'Completed'),
(2, 3, '2023-11-05 10:00:00', '2023-11-10 18:00:00', 275.00, 'Completed'),
(3, 7, '2023-11-12 08:00:00', '2023-11-15 16:00:00', 210.00, 'Confirmed'),
(4, 2, '2023-11-15 11:00:00', '2023-11-17 19:00:00', 100.00, 'Confirmed'),
(5, 5, '2023-11-18 09:00:00', '2023-11-20 17:00:00', 96.00, 'Pending'),
(6, 8, '2023-11-20 10:00:00', '2023-11-25 18:00:00', 450.00, 'Confirmed'),
(7, 4, '2023-11-22 08:00:00', '2023-11-24 16:00:00', 120.00, 'Pending'),
(8, 6, '2023-11-25 11:00:00', '2023-11-30 19:00:00', 375.00, 'Confirmed'),
(9, 9, '2023-12-01 09:00:00', '2023-12-03 17:00:00', 104.00, 'Pending'),
(10, 10, '2023-12-05 10:00:00', '2023-12-10 18:00:00', 325.00, 'Confirmed');

-- Verify data
SELECT 'Customers' AS TableName, COUNT(*) AS RecordCount FROM Customer
UNION ALL
SELECT 'Vehicles', COUNT(*) FROM Vehicle
UNION ALL
SELECT 'Reservations', COUNT(*) FROM Reservation
UNION ALL
SELECT 'Admins', COUNT(*) FROM Admin;