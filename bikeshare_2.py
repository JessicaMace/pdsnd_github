import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA.keys():
        print("\nHi! Which city would you like to explore?")
        print("\nChicago, New York City, or Washington")
        print("\nPlease enter full name of city you wish to explore. \nDon\'t worry, it\'s not case sensitive.")
        city=input().lower()

        if city not in CITY_DATA.keys():
            print("\nOpps! Something doesn\'t match. Please check the spelling.")
            print("\nLet\'s try again.")

    print(f"\nYou picked {city.title()}. Let\'s go exploring!")

    # TO DO: get user input for month (all, january, february, ... , june)
    #need a month dictionary
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA:
        print("\nWhat month would you like to explore? You can choose any month from January to June.")
        print("\nPlease enter the month you would like to see. If you can\'t choose a month, just enter all.")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nUh Oh! Double check the spelling.")
            print("\n Let\'s try again!")

    print(f"\nYou have picked {month.title()}.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    #need a day dictionary
    DAY_LIST = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = ''
    while day not in DAY_LIST:
        print("\nAlmost there! Enter the day of the week would you like to explore.")
        print("\nWant to see the whole week? Just enter all.")
        day = input().lower()

        if day not in DAY_LIST:
            print("\nOh no! Something went wrong.")
            print("\nCheck the spelling and let\'s go again.")

    print(f"\nYou picked {day.title()}.")
    print(f"\nYou want to explore city: {city.upper()}, month: {month.upper()} and day: {day.upper()}. Let\'s Go!")
    print('-'*60)
    return city, month, day

#load data from .csv files
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

#calculate all time related stats
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]

    print(f"\nMost Popular Month (1 = January,...,6 = June): {popular_month}")

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nMost Popular Day: {popular_day}")

    # TO DO: display the most common start hour
    #need the hour
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print(f"\nMost Popular Start Hour: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

#station stats section
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"\nThe most commonly used start station is: {common_start_station}")

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most commonly used end station is: {common_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    #combine columns
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    trip = df['Start To End'].mode()[0]

    print(f"\nThe most common trip is from: {trip}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

#time taken stats
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    #make it more user friendly
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print(f"\nThe total duration of trips is {hour} hours, {minute} mins, and {second} seconds.")

    # TO DO: display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    #makes it easier to comprehend
    mins, secs = divmod(average_duration, 60)
    #what if the average takes over an hour
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is: {hrs} hours, {mins} minutes, and {secs} seconds.")
    else:
        print(f"\nThe average trip duration is: {mins} minutes, and {secs} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#user stats section
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()

    print(f"\nHere is the types of users by number:\n\n{user_type}")

    # TO DO: Display counts of gender
    #account for not all having a gender column
    try:
        gender = df['Gender'].value_counts()
        print(f"\nHere is the types of users by gender:\n\n{gender}")
    except:
        print(f"\nOpps! Looks like there was no gender recorded in this City.")

    # TO DO: Display earliest, most recent, and most common year of birth
    #account for no birth year
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest birth year is: {earliest}\n\nThe most recent birth year is: {recent}\n\nAnd the most common birth year is: {common_year}")
    except:
        print(f"\nOh No! Looks like there was no birth year recorded for this City.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#raw data on request
def display_data(df):
    """Displays 5 rows of raw data from the .csv file for the selected city."""

    RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    #counter to carry on with viewing file if wanted
    counter = 0
    while rdata not in RESPONSE_LIST:
        print("\nWould you like to view the raw data for this City? Yes or no")
        rdata = input().lower()
        if rdata == "yes":
            print(df.head())
        elif rdata not in RESPONSE_LIST:
            print("\nWhoops! Check the spelling and let\'s try again")

    #loop to continue viewing data
    while rdata == 'yes':
        print("Would you like to view more?")
        counter += 5
        rdata = input().lower()
        if rdata == "yes":
            print(df[counter:counter+5])
        elif rdata != "yes":
            break

    print('-'*40)


#hope it ties it all together
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
