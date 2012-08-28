# django-hotlinks

This package includes the Django app hotlinks which makes it easy to 
links to your Django models in your content.

## Installation

Clone the [Git repository](https://github.com/agoodid/django-hotlinks).

## Usage

First register your models and what functions should be available for
linking like this:

    from hotlinks import register
    register(yourmodel)                  # Links to get_absolute_url
    register(yourmodel, "your_function") # Links to your_function

Then, whenever you want to link to those models you can write links as:

    Link to get_absolute_url function [yourapp.yourmodel.1]
    Link to another function [yourapp.yourmodel.1:your_function]
    Link to a function with arguments [yourapp.yourmodel.1:your_function:argument]

And in your template use the hotlinks filter to transform them into HTML links:

    {% load hotlinks %}
    {{ text|hotlinks|safe }}
