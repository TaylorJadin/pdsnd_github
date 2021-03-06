import time
import datetime
import calendar
import pandas as pd
import numpy as np

# specify available cities and their respective csv files here
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# specify which months we have data for
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. For month and day, the user can specify "all" so that load_data() doesn't use a month or day filter.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    cities = list(CITY_DATA.keys())
    cities_str = ", ".join(cities[:-1]).title() + ', or ' + cities[-1].title()
    while city not in cities:
        try:
            city = input('\nChoose a city you would like to see data for:\n    {}\n'.format(cities_str)).lower().strip()
            if city not in cities:
                print('\nInvalid city: Please type the name of a city from the list')
        except Exception as e:
            print("\nException occurred: {}".format(e))

    # get user input for month (all, january, february, ... , june)
    month = ''
    months = MONTHS + ['all']
    months_str = ", ".join(MONTHS[:-1]).title() + ', or ' + MONTHS[-1].title()
    while month not in months:
        try:
            month = input('\nChoose a month you would like to see data for:\n    {}\n    Type "all" to see data for all months. \n'.format(months_str)).lower().strip()
            if month not in months:
                print('\nInvalid month: Please type the name of a month in the list, or "all"')
        except Exception as e:
            print("\nException occurred: {}".format(e))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    days = DAYS + ['all']
    days_str = ", ".join(DAYS[:-1]).title() + ', or ' + DAYS[-1].title()
    while day not in days:
        try:
            day = input('\nChoose a day you would like to see data for: \n    {}\n    Type "all" to see data for all days. \n'.format(days_str)).lower().strip()
            if day not in days:
                print('\nInvalid day: Please type the name of a day, or "all"')
        except Exception as e:
            print("\nException occurred: {}".format(e))


    print('\n', '-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable. If month and/or day is "all" then no month or day filter is applied.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['month_name'] = df['Start Time'].dt.month.apply(lambda x: calendar.month_name[x])

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        common_month = df['month_name'].mode()[0]
        print('\nMost common month:\n    ', common_month)

    # display the most common day of week
    if day == 'all':
        common_day = df['day_of_week'].mode()[0]
        print('\nMost common day:\n    ', common_day)

    # display the most common start hour

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('\nMost Popular Start Hour:\n    ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n', '-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('\nMost commonly used start station:\n    ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nMost commonly used end station:\n    ', common_end_station)

    # display most frequent combination of start station and end station trip
    common_station_combo = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nMost frequent combination of start and end stations:\n')
    print(common_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n', '-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    nice_total_time = str(datetime.timedelta(seconds=int(total_time)))
    print('\nTotal travel time:\n    ', nice_total_time)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    nice_mean_time = str(datetime.timedelta(seconds=int(mean_time)))
    print('\nMean travel time:\n    ', nice_mean_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n', '-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('\nUser types:\n')
    print(user_type_count)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nGender:\n')
        print(gender_count)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print('\nEarliest birth year:\n    ', int(earliest_birth_year))
        latest_birth_year = df['Birth Year'].max()
        print('\nLatest birth year:\n    ', int(latest_birth_year))
        common_birth_year = df['Birth Year'].mode()[0]
        print('\nMost common birth year:\n    ', int(common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n', '-'*40)

def print_loop(df):
    """Prints through the raw data, 5 rows at a time"""
    print_rows = input('\nWould you like to print the first 5 rows of data? Enter yes or no.\n')
    if print_rows.lower().strip() == 'yes':
        start_row = 0
        last_row = 5
        num_of_rows = df.shape[0]
        while last_row < num_of_rows:
            print('-'*40)
            print(df[start_row:last_row])
            print('-'*40)
            start_row += 5
            last_row += 5
            
            print_more = input('\nWould you like to continue with the next 5 rows? Enter yes or no.\n')
            if print_more.lower().strip() != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_loop(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()