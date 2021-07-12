Writing Your Custom Plugs
=========================

How to write your custom plug classes
--------------------------------------

There are examples in pyNodes module itself to help understand how to write
your own custom plug.

Lets take a example of intPlug.

The intPlug.py file can be found in
.../pyNodes/PyNodeEditor/configs/plugs/defaults/floatPlug.py


.. literalinclude:: ../../PyNodeEditor/configs/plugs/defaults/floatPlug.py
    :language: python

You need two classes to begin with

-   InputPlug
-   RegisterInputPlug


Adding **RegisterInputPlug** as decorator to your plug register your plug class
in the network of engine.

**InputPlug** is the core class from which you should always inherit to create
your own plug class.

.. note::
    Even though we are calling our plug class as IntPlug, but we are not
    associating any type to our plug class.
    The type of the plug gets registers when we add them into node with the value.


.. literalinclude:: ../../PyNodeEditor/configs/nodes/math/addition.py
    :language: python

Here in **setup_plugs** method we have used floatPlug and given its default
value a float.


Where to keep your custom plug python files
--------------------------------------------

-   User can write their own custom plugs and keep them in certain locations
    (local, central) which then engine reads and prepare those nodes ready for
    use in creating nodes under network.


-   On Windows you can keep your custom plugs here

    **C:\\Users\\<username>\\Documents\\PyNodeEditor\\configs\\plugs
    \\<category>\\YourPlug.py**


-   On Linux you can keep your custom plugs here
    **../<user>/PyNodeEditor/configs/plugs/<category>/YourPlug.py**


-   You can define a global/central path for the config directory and engine
    will read custom plugs from that dir.
    You need to define a variable called **PYNODE_CONFIG_PATH** and set its
    path to config folder.