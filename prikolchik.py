class Book:
    def __init__(s,title,author,isbn):
     s.title=title
     s.author=author
     s.isbn=isbn

class Library:
    def __init__(s):
      s.books=[]

    def add_book(s):
        title=input("Title: ")
        author=input("Author: ")
        isbn=input("ISBN: ")
        s.books.append(Book(title, author, isbn))
        print(f"Book '{title}' was added to the library")

    def remove_book(s):
        title = input("Enter the title of the book to remove: ")
        for book in s.books:
            if book.title == title:
                s.books.remove(book)
                print(f"Book '{title}' removed from the library")
                return
        print(f"Book '{title}' was not found in the library")

    def display_books(s):
        if not s.books:
            print("No books in the library")
        else:
            print("Books in the library:")
            for book in s.books:
                print(f"Title: {book.title}")
                print(f"Author: {book.author}")
                print(f"ISBN: {book.isbn}")


def main():
    library = Library()

    menu_options = {
        '1': library.add_book,
        '2': library.remove_book,
        '3': library.display_books,
        '4': exit
    }

    while True:
        print("\nMenu:")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Display all books")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice in menu_options:
            menu_options[choice]()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
