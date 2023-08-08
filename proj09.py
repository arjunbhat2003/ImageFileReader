#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 13:42:38 2022
Main:
    prints header
    opens JSON image file and category file using open file function
    creates dictionaries using filepointers amd read file functions
    creates category set using dictionaries
    creates image list dict using dictionaries and set
    prompts for option using get option function
    while option not q:
        if c:
            displays sorted category names seperated by commas
        if f:
            displays sorted category names seperated by commas
            prompts user for category till valid
            displays header with category
            displays list of images in numeroc order
        if i:
            prints max instances of a category in image file
        if m:
            prints the category that appears in the most images
        if w:
            prompts for number of words to display
            loops until valid int above 0
            displays the input amount of words with the top word count in table format
        prompts for another option
    closing statement
            
        
    
"""
#import statements
import json,string
import string
#initializes variables
STOP_WORDS = ['a','an','the','in','on','of','is','was','am','I','me','you','and','or','not','this','that','to','with','his','hers','out','it','as','by','are','he','her','at','its']
MENU = '''
    Select from the menu:
        c: display categories
        f: find images by category
        i: find max instances of categories
        m: find max number of images of categories
        w: display the top ten words in captions
        q: quit
        
    Choice: '''
def get_option():
   ''' 
   prints menu of choices and prompts for user to select one
   loops until valid option input
   returns lower case option
   '''
   option = input(MENU).lower()#prints menu and prompts for option, converts to lowercase
   valid_options = 'cfimwq'#sets valid options as string
   while not option in valid_options:#while option not in valid opt string
       print("Incorrect choice.  Please try again.")#error statement
       option = input(MENU).lower()#prints menu and prompts for option, converts to lowercase
   return option#returns option
def open_file(s):
   ''' 
   prompts for filename to be opened
   tries to open it
   loops until file can be opened
   returns filepointer
   '''
   i = 0#sets variable to exit loop
   while i ==0:#continues loop until variable is changed
       try:
           file_name = input("Enter a {} file name: ".format(s))#prompts for file name with parameter formatted in
           fp = open(file_name,'r')#tries to open the file
           return fp#returns filepointer if file can be opened
           i = 1#changes variable to exit loop
       except FileNotFoundError:
           print("File not found.  Try again.")#error statement if file cannot be opened    
def read_annot_file(fp1):
   ''' 
   creates a dictionary from filepointer
   returns dictionary
   '''
   return json.load(fp1)#returns dictionary created by filepointer
def read_category_file(fp2):
   ''' 
   creates a dictionary from filepointer
   returns dictionary
   '''
   D = {}#initializes dict
   for line in fp2:#goes through each line in filepointer
       temp_list = line.split()#creates temporary list of 2 items for each line
       D[int(temp_list[0])] = temp_list[1]#adds temp list to dictionary as key value pair
   return D#returns dictionary
def collect_catogory_set(D_annot,D_cat):
   ''' 
   creates category set from two dictionaries
   returns cat_set
   '''
   cat_set = set()#initializes set
   for key in D_annot:#goe through each image in dict
       for value in D_annot[key]['bbox_category_label']:#goes through each category label for image
           cat_set.add(D_cat[value])#adds the name of category to set referncing other dict
   return cat_set
def collect_img_list_for_categories(D_annot,D_cat,cat_set):
   ''' 
   creates a dictionary with list as value that has images in list as value and category as key
   returns dictionary of image list for categories
   '''
   D = {}#initalizes dictionary
   for x in cat_set:#goes through each item in category set
       D[x]= []#adds item as key with empty list in dictionary
   for key in D_annot:#goes through each image in dict
       for value in D_annot[key]['bbox_category_label']:#goes through each category label for image
           D[D_cat[value]].append(key)#adds image id to value list with category name as key
   for key in D:#goes through each key in new dict
       D[key].sort()#sorts each value list
   return D#returns dictionary
def max_instances_for_item(D_image):
   ''' 
   finds maximum instances that a category was referenced
   returns tuple of max instances and category
   '''
   return (max(len(value) for value in D_image.values()),[key for key in D_image if len(D_image[key]) == max(len(value) for value in D_image.values())][0])#finds max instance and category and returns in tuple
def max_images_for_item(D_image):
   ''' 
   finds maximum images that a category was referenced
   returns tuple of max number of images and category
   '''
   return (max(len(set(value)) for value in D_image.values()),[key for key in D_image if len(set(D_image[key])) == max(len(set(value)) for value in D_image.values())][0])#finds highest number of images that an item is in and returns number and item as tuple
def count_words(D_annot):
   '''
   finds number of times each word is used in captions
   creates a list of tuples with count and word
   '''
   D = {}#initializes dictionary
   for key in D_annot:#goes through each image
       for value in D_annot[key]['cap_list']:#goes through each caption for each image
           for word in value.split():#goes through each word in list made from caption
               word = word.strip(string.punctuation)#strips punctuation from word
               if word.isalpha() and word not in STOP_WORDS:#if word is all letters and a valid word
                   if word not in D:#if word is not yet in dict
                       D[word]=1#sets value to 1
                   else:#if word is in dict already
                       D[word]+=1#adds one
   count_list = list(zip(D.values(),D.keys()))#creates a list of tuples using values and keys
   count_list.sort(reverse = True)#sorts list by decreasing word cout
   return count_list#returns list
def main():    
    print("Images\n")#header
    fp1 = open_file('JSON image') #gets JSON filepointer using open file function
    D_annot = read_annot_file(fp1)#creates dictionary from JSON filepointer
    fp2 = open_file('category')#gets category filepointer using open file function
    D_cat = read_category_file(fp2)#creates dictionary from category filepointer
    cat_set = collect_catogory_set(D_annot, D_cat)#creates 
    D_image = collect_img_list_for_categories(D_annot, D_cat, cat_set)#creates dictionary using collect image list function
    option = get_option()#prompts for option using get option
    while not option =='q':#while choice isn't quit
        if option =='c':#if choice is c
            new_list = list(cat_set)#creates a list out of category set
            new_list.sort()#sorts list
            cat_str =''#initializes string
            for item in new_list:#goes through each item in list
                cat_str+= item + ', '#adds item to string followed by a comma space
            print("\nCategories:")#prints header
            print(cat_str.strip(', '))#prints stripped string
        if option =='f':#if choice is f
            print("\nCategories:")#header
            print(cat_str.strip(' ,'))#prints stripped string of categories
            cat_opt = input("Choose a category from the list above: ")#prompts for category
            while cat_opt not in cat_set:#error check for valid cat
                print("Incorrect category choice.")#error statement
                cat_opt = input("Choose a category from the list above: ")#reprompts for category
            print("\nThe category {} appears in the following images:".format(cat_opt))#header with input category formatted
            cat_list = D_image[cat_opt]#creates list of image ids for category
            cat_list = [int(item) for item in cat_list]#turns all image ids into int types
            cat_list =list(set(cat_list))#removes duplicates by turning into a set and back to a list
            cat_list.sort()#sorts list
            cat_string= ''#initializes string
            for item in cat_list:#goes through each item in list
                cat_string += str(item) + ', '#adds string of item to string followed by comma space
            print(cat_string.strip(', '))#prints stripped string
        if option =='i':#if choice is i
            max_inst = max_instances_for_item(D_image)#finds max instances using max instances function
            print("\nMax instances: the category {} appears {} times in images.".format(max_inst[1],max_inst[0]))#prints the max instances and the category
        if option == 'm':#if choice is m
            max_image = max_images_for_item(D_image)#finds the max number of one category in an image
            print("\nMax images: the category {} appears in {} images.".format(max_image[1],max_image[0]))#prints the max number and the category
        if option =='w':#if choice is w
            word_count= int(input("\nEnter number of desired words: "))#prompts for number of words to be displayed
            while word_count <= 0:#loops until int >0 input
                print("Error: input must be a positive integer: ")#error statement
                word_count= int(input("\nEnter number of desired words: "))#reprompts number
            count_list = count_words(D_annot)[0:word_count]#creates a list with input numnber of items by referencing count words function
            print("\nTop {} words in captions.".format(word_count))#header with word count formatted
            print("{:<14s}{:>6s}".format("word","count"))#table header
            for tup in count_list:#for tuple in list
                print("{:<14s}{:>6d}".format(tup[1],tup[0]))#prints items of tuple in table format
        option = get_option()#reprompts for option
    print("\nThank you for running my code.") #closing statement
# Calls main() if this modules is called by name
if __name__ == "__main__":
    main()     