import argparse

def guess_number():
    """Guess the number function."""
    
    import random

    print('Welcome to the Guess the Number game!')
    print('I\'m thinking of a number between 1 and 100.')
    print('Try to guess it in as few attempts as possible.')

    # The random function returns a floating point number, so I'm converting it to an integer with the int function
    the_number = random.randint(1, 100)
    guess = int(input('Take a guess: '))
    tries = 1

    while guess != the_number:
        if guess > the_number:
            print('Lower...')
        else:
            print('Higher...')
        guess = int(input('Take a guess: '))
        tries += 1

    print('You guessed it! The number was', the_number)
    print('And it only took you', tries, 'tries!')

def square_number():
    parser = argparse.ArgumentParser(description='Square a number')
    parser.add_argument("square", help="display a square of a given number", type=int)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbosity", action="store_true", help="increase output verbosity")
    group.add_argument("-q", "--quiet", action="store_true", help="decrease output verbosity")

    args = parser.parse_args()
    answer = args.square**2

    if args.verbosity:
        print("the square of {} equals {}".format(args.square, answer))
    elif args.quiet:
        print(answer)
    else:
        print("{}^2 == {}".format(args.square, answer))
