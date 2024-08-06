class Book:
    def __init__(self, title, category, rating, price, stock):
        # Validate the tittle is not empty
        if not title:
            raise ValueError("Title cannot be empty")
        # Validate the category is not empty
        if not category:
            raise ValueError("Category cannot be empty")
        # Validate that the rating is between 0 and 5
        if not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        # Validate that the price is not negative
        if price < 0:
            raise ValueError("Price cannot be negative")
        # Validate that the stock is not negative
        if stock < 0:
            raise ValueError("Stock cannot be negative")
        # Private attributes to store book information
        self.__title = title
        self.__category = category
        self.__rating = rating
        self.__price = price
        self.__stock = stock

    # Getters
    @property
    def title(self):
        """Returns the title of the book."""
        return self.__title

    @property
    def category(self):
        """Returns the category of the book."""
        return self.__category

    @property
    def rating(self):
        """Returns the rating of the book."""
        return self.__rating

    @property
    def price(self):
        """Returns the price of the book."""
        return self.__price

    @property
    def stock(self):
        """Returns the stock quantity of the book."""
        return self.__stock


    # Setters
    @title.setter
    def title(self, title):
        """Sets the category of the book, ensuring it is not empty."""
        if not title:
            raise ValueError("Title cannot be empty")    
        self.__title = title

    @category.setter
    def category(self, category):
        """Sets the category of the book, ensuring it is not empty."""
        if not category:
            raise ValueError("Category cannot be empty")
        self.__category = category

    @rating.setter
    def rating(self, rating):
        """Sets the rating of the book, ensuring it is between 0 and 5."""
        if 0 <= rating <= 5:
            self.__rating = rating
        else:
            raise ValueError("Rating must be between 0 and 5")

    @price.setter
    def price(self, price):
        """Sets the price of the book, ensuring it is not negative."""
        if price >= 0:
            self.__price = price
        else:
            raise ValueError("Price cannot be negative")

    @stock.setter
    def stock(self, stock):
        """Sets the stock quantity of the book, ensuring it is not negative."""
        if stock >= 0:
            self.__stock = stock
        else:
            raise ValueError("Stock cannot be negative")