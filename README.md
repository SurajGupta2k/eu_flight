# ✈️ EU Flight Monitor

A comprehensive system for monitoring flights across European airports and tracking delays for passenger compensation claims.

## Overview

EU Flight Monitor is a Flask-based API that collects, stores, and provides real-time flight information from European airports. The system is designed to help identify flights delayed by more than 2 hours, assisting passengers in filing compensation claims under EU regulations.

## Features

- Real-time flight monitoring across European airports
- Automatic delay detection and tracking
- Comprehensive airport database with IATA/ICAO codes
- RESTful API for accessing flight data
- Integration with Aviation Stack API for live flight data

## System Architecture

### Database Schema

The system uses MySQL with the following main tables:
- `airports`: Stores European airport information (IATA/ICAO codes, location, etc.)
- `airlines`: Airlines operating in Europe
- `flights`: Flight schedules and status
- `flight_status`: Possible flight statuses
- `flight_status_updates`: Historical tracking of flight status changes

### Data Collection Strategy

1. **Airport Data**:
   - Primary source: Curated JSON database (`airports.json`)
   - Regular updates through aviation authorities' official data
   - Manual verification for data accuracy

2. **Flight Data**:
   - Real-time data from Aviation Stack API
   - Periodic polling (every 5-15 minutes)
   - Backup data sources for redundancy

3. **Delay Monitoring**:
   - Continuous tracking of flight status updates
   - Automatic flagging of delays > 120 minutes
   - Historical delay data maintenance

## API Endpoints

### Airport Information
- `GET /airports`: List all European airports
- `GET /airports/{airport_code}/flights`: Get flights for specific airport

### Flight Monitoring
- `GET /api/flights/live`: Get real-time flight data
- `GET /flights/delayed`: List flights delayed > 2 hours
- `GET /flights/active`: List all active flights
- `GET /flights/{flight_id}`: Get specific flight details
- `GET /flights/search/{flight_number}`: Search flight by number

### Statistics
- `GET /api/stats/delays`: Get delay statistics by airline

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   MYSQL_USER=your_user
   MYSQL_PASSWORD=your_password
   MYSQL_HOST=your_host
   MYSQL_DATABASE=your_database
   AVIATION_STACK_API_KEY=your_api_key
   ```
4. Initialize the database:
   ```bash
   flask db upgrade
   ```
5. Run the application:
   ```bash
   python eu_flight/src/app.py
   ```

## Data Accuracy and Maintenance

- Regular data validation against multiple sources
- Automated tests for data consistency
- Manual verification of critical updates
- Backup systems for data redundancy

## Security Measures

- API key authentication
- Rate limiting
- HTTPS encryption
- Regular security audits
- Data backup and recovery procedures

## Future Enhancements

1. Machine learning for delay prediction
2. Mobile app for passenger notifications
3. Integration with airline compensation systems
4. Extended coverage to non-EU airports
5. Real-time weather impact analysis

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🌟 Key Features

- **Real-time Flight Tracking**
  - Live flight status updates via Aviation Stack API
  - Comprehensive flight details including delays, gates, and terminals
  - Support for filtering by airline and limiting results
  - Real-time status monitoring and updates
  - Automatic delay detection and tracking

- **Cloud Database Integration**
  - Integrated with freesqldatabase.com for cloud storage
  - Automatic data synchronization between API and database
  - Real-time data persistence for all flight updates
  - Scalable cloud-based storage solution
  - Secure remote database access

- **Airport Management**
  - Database of European airports with IATA/ICAO codes
  - Geographical information including coordinates and timezones
  - Flight schedules for specific airports
  - Interactive airport search and filtering

## 🗄️ Database Configuration

### Cloud Database Setup
The project uses freesqldatabase.com for data storage. Configuration:

```env
MYSQL_USER=your_freesql_username
MYSQL_PASSWORD=your_freesql_password
MYSQL_HOST=sql12.freesqldatabase.com
MYSQL_DATABASE=your_database_name
```

### Database Schema
Tables are automatically created in the cloud database:
- `flight_status`: Stores possible flight statuses
- `airports`: European airport information
- `airlines`: Airline details
- `flights`: Flight records
- `flight_status_updates`: Real-time status changes

### Data Flow
1. Aviation Stack API provides real-time flight data
2. Data is processed by Flask backend
3. Information is stored in freesqldatabase.com
4. API endpoints serve data from cloud database
5. Real-time updates maintain data consistency

## 🔄 Data Synchronization

The system maintains real-time synchronization between:
- Aviation Stack API (data source)
- freesqldatabase.com (cloud storage)
- API endpoints (data access)

Key synchronization points:
- `/api/flights/live`: Fetches and stores real-time data
- Status updates are immediately persisted
- Historical data is maintained for analysis
- Automatic conflict resolution for concurrent updates

### 5. Deploy to Vercel (Recommended)

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy the application:
   ```bash
   vercel
   ```

4. For production deployment:
   ```bash
   vercel --prod
   ```

The application is already configured for Vercel deployment with the `vercel.json` file. Vercel will:
- Automatically detect your Python application
- Install dependencies from `requirements.txt`
- Set up serverless functions
- Deploy with environment variables
- Provide a unique URL for your application

#### Vercel Deployment Features
- Zero configuration required
- Automatic HTTPS
- Continuous deployment from GitHub
- Serverless architecture
- Built-in CDN
- Real-time logs and monitoring

#### Environment Variables on Vercel
You can set environment variables in the Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variables (replace with your actual values):
   ```
   MYSQL_USER=your_database_user
   MYSQL_PASSWORD=your_database_password
   MYSQL_HOST=your_database_host
   MYSQL_DATABASE=your_database_name
   AVIATION_API_KEY=your_api_key
   ```

⚠️ **Security Note**: Never commit sensitive credentials to version control. Always use environment variables for sensitive information. 

