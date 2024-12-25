class Article:
    all = []

    def __init__(self, author, magazine, title):
        # Validate at construction time
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")

        self._author = author
        self._magazine = magazine
        self._title = title

        Article.all.append(self)

    @property
    def title(self):
        return self._title  # Should remain immutable

    @title.setter
    def title(self, value):
        """
        IMMUTABLE according to the tests:
          - They try to do `article_1.title = 500`
          - Then assert that it remains the old title.
          - They do NOT want an exception; they want to silently ignore.
        """
        # Simply ignore any assignment attempt.
        pass

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        # The tests do want us to allow changing the author,
        # but only if it's an Author instance. If not, do nothing.
        if isinstance(value, Author):
            self._author = value
        # else ignore invalid assignment

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        # The tests do want us to allow changing the magazine,
        # but only if it's a Magazine instance. If not, do nothing.
        if isinstance(value, Magazine):
            self._magazine = value
        # else ignore invalid assignment

    @classmethod
    def get_all(cls):
        return cls.all


class Author:
    def __init__(self, name):
        # Validate at construction time
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")
        self._name = name

    @property
    def name(self):
        return self._name  # Should remain immutable

    @name.setter
    def name(self, value):
        """
        IMMUTABLE according to the tests:
          - They try `author_1.name = "ActuallyTopher"` then `assert author_1.name == "Carry Bradshaw"`.
          - They do NOT want an exception; they want us to silently ignore the assignment.
        """
        # Silently ignore any attempt to reset the name.
        pass

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list(set(article.magazine for article in self.articles()))

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        areas = list(set(magazine.category for magazine in self.magazines()))
        return areas if areas else None


class Magazine:
    all = []

    def __init__(self, name, category):
        # Validate at construction time
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")

        self._name = name
        self._category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """
        MUTABLE according to tests:
          - If valid (str of length 2-16), update.
          - If invalid, ignore (so that we don't raise an exception, and
            the tests confirm that the name remains unchanged).
        """
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        # else do nothing (ignore invalid assignment)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        """
        MUTABLE according to tests:
          - If valid (non-empty string), update.
          - If invalid, ignore so that the value remains unchanged.
        """
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # else do nothing (ignore invalid assignment)

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list(set(article.author for article in self.articles()))

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        """
        returns authors who have written more than 2 articles for this magazine
        """
        authors = [article.author for article in self.articles()]
        return [author for author in set(authors) if authors.count(author) > 2] or None

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        magazine_article_count = {mag: len(mag.articles()) for mag in cls.all}
        return max(magazine_article_count, key=magazine_article_count.get)
