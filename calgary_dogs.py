# calgary_dogs.py
# Austen Zhang
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd
import numpy as np

def percentage_of_registrations_by_year(data_multi_index, year, breed_selection):
    '''
    Prints the percentage of registrations of selected breed in selected year out of total registrations in selected year.

    Parameters:
        data_multi_index: pandas dataframe of data with multi-index of month and year
        year: the selected year to calculate percentage
        breed_selection: the selected dog breed from user input

    '''
    idx = pd.IndexSlice # creating IndexSlice object so we can select rows with just the year in question
    breed_registrations_year = np.nansum(data_multi_index.loc[data_multi_index['Breed'] == breed_selection].loc[idx[year,:], 'Total']) #using mask to filter out unselected dog breeds, then selecting rows corresponding to appropriate year and only selecting the 'Total' column to calculate sum.
    total_registrations_year = np.nansum(data_multi_index.loc[idx[year,:], 'Total']) # summing up all registrations for a given year
    percentage = breed_registrations_year/total_registrations_year*100 # calculating percentage with registrations of selected breed in selected year divided by total registrations for the year.
    print(f"The {breed_selection} was {percentage:.6f}% of top breeds in {year}.") # printing percentage to 6 decimal places as shown in screenshot.


def main():

    # Importing data from CalgaryDogBreeds.xlsx file
    data = pd.read_excel('CalgaryDogBreeds.xlsx', sheet_name='Sheet1')

    print("ENSF 692 Dogs of Calgary")

    # User input stage
    breed_selection = 0
    
    while True: # while loop to repeat prompting for user input if input is invalid
        try:
            breed_selection = input("Please enter a dog breed: ").lower() #prompting for user input, then converting resulting string to lower case.
            for breed in data['Breed']: #looping through 'Breed' column in dataframe.
                if breed.lower() == breed_selection: #if input matches value in dataframe (converted to lowercase), change input to match upper and lower case of dataframe, and break out of for loop.
                    breed_selection = breed
                    break
            else: #for-else loop used. If no break in the for loop, it means there was no match, meaning input was invalid.
                raise KeyError() #Raising value error with a clarifying message.
        except KeyError:
            print('Dog breed not found in the data. Please try again') # Printing value error message and restart while loop.
        else:
            break # if no ValueError, it means the user input matched a breed in the dataframe, and we can break out of the while loop.

    # Data anaylsis stage

    data_multi_index = data.set_index(['Year', 'Month']).sort_index() #creating multiindex version of dataframe
    data_breed = data_multi_index.loc[data_multi_index['Breed'] == breed_selection] # creating dataframe with unselected dog breed already filtered out

    #Years in top breeds
    years_in_top_breeds = set() #Create set, this is to ensure no repeat of years once it has already been added to the set.
    for year in data.loc[data['Breed'] == breed_selection]['Year']: #using mask to select entries in dataframe that correspond to selected breed. Then only selected values in the 'Year' column.
        years_in_top_breeds.add(year) # add the value in the year column to the set.
    print(f"The {breed_selection} was found in the top breeds for years: ", end = "")
    print(*years_in_top_breeds)

    # Total # of registrations of the selected breed found in the dataset.
    breed_registrations = np.nansum(data_breed['Total']) # using data_breed dataframe, which already has unselected dog breeds filtered out, sum up total column to get registrations of selected breed.
    print(f"There have been {breed_registrations} {breed_selection} dogs registered total.")

    # Percentage of selected breed registrations out of the total percentage for each year.
    #2021
    percentage_of_registrations_by_year(data_multi_index, 2021, breed_selection)
    #2022
    percentage_of_registrations_by_year(data_multi_index, 2022, breed_selection)
    #2023
    percentage_of_registrations_by_year(data_multi_index, 2023, breed_selection)

    # Percentage of selected breed registrations out of the total three year percentage.
    total_registrations = np.nansum(data_multi_index['Total']) # calculating total registrations on entire dataset
    percentage = breed_registrations / total_registrations * 100 # computing percentage by dividing registrations of selected breed by total registrations.
    print(f"The {breed_selection} was {percentage:.6f}% of top breeds across all years.") # printing percentage to 6 decimal places.

    # Months that were most popular for the selected breed registrations. This will be done based on registrations of the month, rather than how many times it appears throughout the years. This method will not match the screenshot but I checked with the instructor and she agrees this is a better approach.
    grouping_months = data_breed.groupby('Month')['Total'].sum() #using groupby to combine months together so total registrations shown for a month across all years.
    max_registrations = np.max(grouping_months) # determining maximum registrations
    max_mask = grouping_months == max_registrations # creating mask for items in series that match max_registrations
    most_popular_months = grouping_months[max_mask].keys() # applying mask to grouping_months Pandas Series to get array of just indexes, which should correspond to the most popular months.
    print(f"Most popular month(s) for {breed_selection} dogs: ", end = "") 
    print(*most_popular_months)



if __name__ == '__main__':
    main()
