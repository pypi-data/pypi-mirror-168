.. _tutorial_enumerate_structures:
.. highlight:: python
.. index::
   single: Tutorial; Enumerate structures

Enumerating structures
======================

Predicting mixing energies
--------------------------

In this step the cluster expansion constructed :ref:`previously
<tutorial_construct_cluster_expansion>` will be employed to predict the mixing
energies for a larger set of structures that are obtained by enumeration. After
loading the CE from file, we loop over all structures with up 12 atoms in the
unit cell and compile silver concentrations and predicted mixing energy into a
list, which is calculated by calling the :func:`predict
<icet.ClusterExpansion.predict>` method of the :class:`ClusterExpansion
<icet.ClusterExpansion>` object with the :class:`ASE Atoms <ase.Atoms>` object
that represents the present structure as input argument.

.. literalinclude:: ../../../examples/tutorial/3_enumerate_structures.py
   :start-after: # step 1
   :end-before: # step 2


Extracting the convex hull
--------------------------

Using this set of mixing energies we then generate the convex hull using the
:class:`ConvexHull <icet.tools.convex_hull.ConvexHull>` class.

.. literalinclude:: ../../../examples/tutorial/3_enumerate_structures.py
   :start-after: # step 2
   :end-before: # step 3


Plotting the results
--------------------

The predicted energies can be plotted together with the convex hull as a
function of the concentration.

.. literalinclude:: ../../../examples/tutorial/3_enumerate_structures.py
   :start-after: # step 3
   :end-before: # step 4

The figure thus generated is shown below.

.. figure:: _static/mixing_energy_predicted.png

  Predicted mixing energies versus concentration for a set of systematically
  enumerated structures.


Filtering for low energy structures
-----------------------------------

The :class:`ConvexHull <icet.tools.convex_hull.ConvexHull>` class also provides some
convenience functions including e.g., the possibility to extract the indices of the
structures that are within a certain distance of the convex hull.

.. literalinclude:: ../../../examples/tutorial/3_enumerate_structures.py
   :start-after: # step 4

These structures can then be calculated for example using the reference method
of choice.


Source code
-----------

.. container:: toggle

    .. container:: header

       The complete source code is available in
       ``examples/tutorial/3_enumerate_structures.py``

    .. literalinclude:: ../../../examples/tutorial/3_enumerate_structures.py
