import time
import pandas as pd
import numpy as np

CITY_DATA = { 'c': 'chicago.csv',
              'n': 'new_york_city.csv',
              'w': 'washington.csv' }
month_list = ('all','jan','feb','mar','apr','may','jun')
day_list = ('all','mon','tue','wed','thu','fri','sat','sun')    
raw_data_list = ('yes','no')
intervals = ('month','day','hour')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    In addition the user is asked if he likes to see 5 rows of raw data.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) raw_data - defines if the user wants to see raw data before statistics
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = month = day = raw_data = ""
    
    while city.lower() not in CITY_DATA:#'c','n','w'):
        if city != "":
            print("{} is not a valid option!".format(city))
        city = input("Please enter the city you want data for. Options are: Chicago(c), New York City(n) or Washington(w):\n")
    
    while month.lower() not in month_list: #('all','jan','feb','mar','apr','may','jun'):
        if month != "":
            print("{} is not a valid option!".format(month))
        month = input("Please enter the month you want data for. Options are: jan, feb, mar, apr, may, jun or all:\n")
    
    while day.lower() not in day_list: #('all','mon','tue','wed','thu','fri','sat','sun'):
        if day != "":
            print("{} is not a valid option!".format(day))
        day = input("Please enter the day you want data for. Options are: mon, tue, wed, thu, fri, sat, sun or all:\n")
    while raw_data.lower() not in raw_data_list: #('yes','no'):
        if raw_data != "":
            print("{} is not a valid option!".format(raw_data))
        raw_data = input("Do you want to see 5 rows of raw data before the statistics are calculated? yes or no? \n")    
    print('-'*40)
    return city, month, day, raw_data


def load_data(city, month, day, raw_data):
    
    """
    Loads data for the specified city and filters by month and day if applicable.
    After the data is loaded the top 5 rows of raw data is printed if the user agreed to this option.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    # convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # add some columns for easier access and aggregation
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day'] = df['Start Time'].dt.weekday_name.str.lower()
    df['hour'] = df['Start Time'].dt.hour
    df['city'] = city.lower()
    
    if month.lower() != 'all':
        df = df[df['month'].str[:3] == month]     
       
    if day.lower() != 'all':
        df = df[df['day'].str[:3] == day]
   
    if raw_data.lower() == 'yes':
        print('Here comes the raw data: \n{}'.format(df.head()))

        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    for i in intervals:
        if i in df.columns:
            most_common = df[i].mode()[0]
            rental_count = df[df[i] == most_common].count()[0]
            print("The most common {} is {} with a total rental count of {}.".format(i,most_common,rental_count))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    most_common_start_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]
    most_common_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    
    print("\nThe most common start station is {}.".format(most_common_start_station))
    print("\nThe most common end station is {}.".format(most_common_end_station))
    print("\nThe most popular trip is from {} to {}.".format(most_common_combination[0],most_common_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # uses the defined function format_travel_time
    print("\nThe total travel time is {}.".format(format_travel_time(df["Trip Duration"].sum())))
    print("\nThe mean  travel time is {}.".format(format_travel_time(df["Trip Duration"].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def format_travel_time(seconds):
    """takes seconds as input and returns a formatted string like this: 4296 day(s) 2 hour(s) 39 minute(s) 45 second(s)"""
    seconds = int(seconds)
    formatted_string = ""
    days = int(seconds / 86400) 
    seconds = seconds % 86400
    hours = int(seconds / 3600)
    seconds %= 3600
    minutes = int(seconds/60)
    seconds %= 60
    if days >= 1:
        formatted_string = str(days) + ' day(s) '
    formatted_string += str(hours) + ' hour(s) ' + str(minutes) + ' minute(s) ' + str(seconds) + ' second(s)'
    return formatted_string

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    
    print("Following user type counts are within the data: {}".format(user_types.to_dict()))
    
    # kind of exception handling, since it is known that washington has no specific customer data
    if df['city'].iloc[0] == 'w':
        print('\nWashington customers don\'t have age or gender data!')
    else:
        gender  = df['Gender'].value_counts()
        print("Following gender counts are within the data: {}".format(gender.to_dict())) 
        min_birth = int(df['Birth Year'].min())
        max_birth = int(df['Birth Year'].max())
        common_birth = int(df.groupby(['Birth Year']).size().idxmax())
        print("The earliest date of birth is {}, the most recent is {} and the most common is {} ".format(min_birth,max_birth,common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
   

    """Testing all possibilities
    
    for city in CITY_DATA:
         for month in month_list:
                for day in day_list:
                    for raw_data in raw_data_list:
                        
                        try:
                            df = load_data(city, month, day, raw_data)
                            time_stats(df)
                        except:
                            print(city,month,day,raw_data)
                            break
      """                   
    while True:
        city, month, day, raw_data = get_filters()
        df = load_data(city, month, day, raw_data)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
