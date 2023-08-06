.. _advanced_topics_get_cluster_vector:
.. highlight:: python
.. index::
   single: Advanced topics; Cluster vectors

Cluster vectors
===============

Although the calculation of cluster vectors is usually handled internally in
:program:`icet`, it is sometimes advantageous to explicitly look at the
cluster vector for structures of interest. This tutorial demonstrates how this
can be carried out in practice.

Import modules
--------------

First, one needs to import the class :class:`~icet.ClusterSpace`
class, which is used to store information regarding a given cluster
space. Additionally, the `ASE <https://wiki.fysik.dtu.dk/ase>`_
function :func:`~ase.build.bulk` will be needed to generate the
structures.

.. literalinclude:: ../../../examples/advanced_topics/get_cluster_vectors.py
   :start-after: # Import modules
   :end-before: # Create a primitive structure

Generate prototype structure
----------------------------

The next step is to build a prototype structure, here a bulk silicon unit cell.
It is furthermore decided that the cluster vectors will be created by
populating the sites with either silicon or germanium. Also, the cutoffs for
pairs, triplets and quadruplets are all set to 5 Å.

.. literalinclude:: ../../../examples/advanced_topics/get_cluster_vectors.py
   :start-after: # and quadruplets (5.0
   :end-before: # Initiate and print

Initialize cluster space
------------------------

The cluster space is created by initiating a
:class:`~icet.ClusterSpace` object and providing the prototype
structure, cutoffs and list elements defined previously as
arguments. Next, we print all relevant information regarding the
cluster space in tabular format.

.. literalinclude:: ../../../examples/advanced_topics/get_cluster_vectors.py
   :start-after: # Initiate and print
   :end-before: # Generate and print the cluster vector for a pure Si

Specifically, the final call should produce the following (partial)
output::

  ------------------------- Cluster Space -------------------------
  subelements: Si Ge
  cutoffs: 5.0 5.0 5.0
  number of orbits: 22
  -----------------------------------------------------------------
  order |  radius  | multiplicity | index | orbit |    MC vector
  -----------------------------------------------------------------
    0   |   0.0000 |        1     |    0  |   -1
    1   |   0.0000 |        2     |    1  |    0  |    [0]
    2   |   1.1756 |        4     |    2  |    1  |  [0, 0]
    2   |   1.9198 |       12     |    3  |    2  |  [0, 0]
  ...
    4   |   2.5525 |        8     |   21  |   20  | [0, 0, 0, 0]
  -----------------------------------------------------------------


Cluster vector for monoelemental supercell
------------------------------------------

After building a new structure in the form of a
:math:`2\times2\times2` supercell, the cluster vectors are constructed
using the :meth:`~icet.ClusterSpace.get_cluster_vector` method for the
instance of the :class:`~icet.ClusterSpace` class that was initiated
in the previous section. The cluster vectors are printed, as a
sequence of tables, as follows:

.. literalinclude:: ../../../examples/advanced_topics/get_cluster_vectors.py
   :start-after: # Generate and print the cluster vector for a pure Si
   :end-before: # Generate and print the cluster vector for a mixed Si-Ge

These lines ought to yield the following result::

  [1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

Cluster vector for alloy supercell
----------------------------------

Finally, the steps described in the previous section are repeated after
substituting one of the Si atoms in the supercell with Ge.

.. literalinclude:: ../../../examples/advanced_topics/get_cluster_vectors.py
   :start-after: # Generate and print the cluster vector for a mixed Si-Ge

In this case the output should be::

  [1.0, -0.875, 0.75, 0.75, 0.75, -0.625, -0.625, -0.625, -0.625, -0.625, -0.625, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

Notice that the first element is always 1.0. This is true for all
cluster vectors constructed in icet. This orbit is called a zerolet
and it is useful when fitting a cluster expansion among other things.

Source code
-----------

.. container:: toggle

    .. container:: header

       The complete source code is available in
       ``examples/get_cluster_vectors.py``

    .. literalinclude:: ../../../examples/advanced_topics/get_cluster_vectors.py
