Introduction
============

Understanding Basic Concepts of pyNode framework
------------------------------------------------

* Framework naming conventions

.. image:: /resource_images/conventions.png
  :width: 500

* Node

   | Node is a basic unit of this framework.
   | Node consists 3 basic components.

      | 1.Input Plugs
      | 2.OutputPlug
      | 3.Computation method


* Connection

   | Connection is relation between two plugs.
   | There are some rules for how connections can be made to avoid cyclic
   | errors.

   | 1. Connection can be made only if source plug is Output type of plug.
   | 2. Connection cant be made in between same type of plugs i.e. Input or
      Output.
   | 3. Connection cant be made if source plug is in downstream dependencies
   | of destination plug.

* Network

   | Network is web of nodes and their relationships.
   | Network keeps tracks of all its nodes.
   | Every node needs to register with Network on creation.
   | Network can be exported and imported into applications.

* Engine

   | The core of pyNode is its Engine.
   | Engine configures the app and registers all nodes, plugs and make them
   | available to API.

