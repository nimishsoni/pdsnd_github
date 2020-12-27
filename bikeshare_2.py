import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city=str(input("Input the City from the list: chicago, new york city, washington: "))
            city=city.lower()
            if city in CITY_DATA.keys():
                break
            else:
                print("Please enter a valid city")
        except:
            print("Please enter a valid city")
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month=str(input("Select the Month for Analyzing Data (January - June) or All for Analyzing all month_list data: "))
            month=month.lower()
            if month in month_list:
                break
            else:
                print("Please enter a valid month")
        except:
            print("Please enter a valid month")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day=str(input("Select the Day of the Week for Analyzing Data or All for Analyzing all day_list data: "))
            day=day.lower()
            if day in day_list:
                #print("You successfully entered a valid Day of the Week")
                break
            else:
                print("Please enter a valid Day of the Week")
        except:
            print("Please enter a valid Day of the Week")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    # filter by month if applicable
    if month != 'all':
        # use the index of the month_list list to get the corresponding int
        month = month_list.index(month)+1
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe

        day = day_list.index(day)
        df = df.loc[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    frequent_month_no = df['month'].value_counts().idxmax() - 1
    frequent_month = month_list[frequent_month_no]
    print("The Most common month of Travel is: ", frequent_month)

    # display the most common day of week
    frequent_day_no = df['day_of_week'].value_counts().idxmax()
    frequent_day = day_list[frequent_day_no]
    print("\nThe Most common day of the week for Travel is: ", frequent_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("\nThe Most frequent start hour for Travel is: ", df['hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The Most commonly used start station is: \n", df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("The Most commonly used end station is: \n", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    Frequent_Station = (df['Start Station'] + "," + df['End Station']).mode()[0]
    print("The Most commonly used combination of start and end station is: ", Frequent_Station.split(","))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time is {} seconds\n".format(df['Trip Duration'].sum()))

    # display mean travel time
    print("Avergage Travel Time is {} seconds\n".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Ride Counts based on User Type are:\n", df['User Type'].value_counts())
    if(city=='chicago' or city=='new york city'):
    # Display counts of gender
        print("\nRide Counts based on Gender are:\n", df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
        print("\nYear of Birth:\n Earliest: {}\n Most Recent:{}\n Most Common:{}\n".format(df['Birth Year'].min(), df['Birth Year'].max(),df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displaying of raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    next = 0
    while True:
        view_data = input('\n Would you like to view More Raw Data:(Yes or No)\n')
        if view_data.lower() != 'yes':
            return
        print(df.iloc[next:next+5])
        next = next + 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
