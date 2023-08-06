def palindrome(A):
    ''' This function is used to create check if a string is a palindrome or not'''
    if A == A[::-1]:
        return 'It is palindromes'
    else:
        return 'it is not a palindrome'

