


with GNATCOLL.Refcount;

with Langkit_Support.Iterators;
private with Langkit_Support.Tree_Traversal_Iterator;

with Librflxlang.Analysis; use Librflxlang.Analysis;
with Librflxlang.Common;   use Librflxlang.Common;






--  This package provides an interface to iterate on nodes in parse trees and
--  to look for node patterns.
--
--  First, as an alternative to ``Librflxlang.Analysis.Traverse``, you can
--  do:
--
--  .. code-block:: ada
--
--     declare
--        It   : Traverse_Iterator'Class := Traverse (My_Unit.Root);
--        Node : RFLX_Node;
--     begin
--        while It.Next (Node) loop
--           --  Process Node
--        end loop;
--     end;
--
--  Now, if you are exclusively looking for nodes whose text is either ``foo``
--  or ``bar``, you can replace the call to ``Traverse`` with the following:
--
--  .. code-block:: ada
--
--        Find (My_Unit.Root, Text_Is ("foo") or Text_Is ("bar"));
--
--  The ``Find``-like functions below take as a second argument a *predicate*,
--  which is an object that can decide if a node should be processed or not.
--  This package provides several built-in predicates (``Kind_Is``,
--  ``Text_Is``, etc.), then you can either define your own, derivating the
--  ``RFLX_Node_Predicate_Interface`` type, or compose them using Ada's boolean operators.

package Librflxlang.Iterators is

   use Support.Text;

   --------------------
   -- Iterators core --
   --------------------

   package RFLX_Node_Iterators is new Support.Iterators
     (Element_Type  => RFLX_Node,
      Element_Array => RFLX_Node_Array);

   type Traverse_Iterator is new RFLX_Node_Iterators.Iterator with private;
   --  Iterator that yields nodes from a tree

   function Traverse (Root : RFLX_Node'Class) return Traverse_Iterator'Class;
   --  Return an iterator that yields all nodes under ``Root`` (included) in a
   --  prefix DFS (depth first search) fashion.

   ---------------------
   -- Predicates core --
   ---------------------

   type RFLX_Node_Predicate_Interface is interface;
   --  Predicate on nodes.
   --
   --  Useful predicates often rely on values from some context, so predicates
   --  that are mere accesses to a function are not powerful enough. Having a
   --  full interface for this makes it possible to package both the predicate
   --  code and some data it needs.
   --
   --  Note that predicates are not thread-safe: make sure you don't use a
   --  predicate from multiple threads, as they can contain caches.

   function Evaluate
     (P : in out RFLX_Node_Predicate_Interface; N : RFLX_Node) return Boolean is abstract;
   --  Return the value of the predicate for the ``N`` node

   package RFLX_Node_Predicate_References is new
      GNATCOLL.Refcount.Shared_Pointers (RFLX_Node_Predicate_Interface'Class);

   subtype RFLX_Node_Predicate is RFLX_Node_Predicate_References.Ref;
   --  Ref-counted reference to a predicate

   type RFLX_Node_Predicate_Array is array (Positive range <>) of RFLX_Node_Predicate;

   function "not" (Predicate : RFLX_Node_Predicate) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes that are *not* accepted by
   --  ``Predicate``.
   --
   --% belongs-to: RFLX_Node_Predicate

   function "and" (Left, Right : RFLX_Node_Predicate) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes that are accepted by both
   --  ``Left`` and ``Right``.
   --
   --% belongs-to: RFLX_Node_Predicate

   function "or" (Left, Right : RFLX_Node_Predicate) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes that are accepted by ``Left``
   --  or ``Right``.
   --
   --% belongs-to: RFLX_Node_Predicate

   function For_All (Predicates : RFLX_Node_Predicate_Array) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes that are accepted by all
   --  given ``Predicates``.
   --
   --% belongs-to: RFLX_Node_Predicate

   function For_Some (Predicates : RFLX_Node_Predicate_Array) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes that are accepted by at least
   --  one of the given ``Predicates``.
   --
   --% belongs-to: RFLX_Node_Predicate

   function For_All_Children
     (Predicate : RFLX_Node_Predicate; Skip_Null : Boolean := True) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes for which ``Predicate``
   --  accepts all children. Unless ``Skip_Null`` is false, this does not
   --  evaluate the predicate on null children.
   --
   --% belongs-to: RFLX_Node_Predicate

   function For_Some_Children
     (Predicate : RFLX_Node_Predicate; Skip_Null : Boolean := True) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes for which ``Predicate``
   --  accepts at least one child. Unless ``Skip_Null`` is false, this does not
   --  evaluate the predicate on null children.
   --
   --% belongs-to: RFLX_Node_Predicate

   function Child_With
     (Field     : Syntax_Field_Reference;
      Predicate : RFLX_Node_Predicate) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes which have a child
   --  corresponding to the given field reference and for which this child is
   --  accepted by the given predicate.
   --
   --% belongs-to: RFLX_Node_Predicate

   ---------------------------
   -- Node search functions --
   ---------------------------

   function Find
     (Root      : RFLX_Node'Class;
      Predicate : access function (N : RFLX_Node) return Boolean := null)
      return Traverse_Iterator'Class;
   --  Return an iterator that yields all nodes under ``Root`` (included) that
   --  satisfy the ``Predicate`` predicate.

   function Find
     (Root : RFLX_Node'Class; Predicate : RFLX_Node_Predicate'Class)
      return Traverse_Iterator'Class;
   --  Return an iterator that yields all nodes under ``Root`` (included) that
   --  satisfy the ``Predicate`` predicate.

   function Find_First
     (Root      : RFLX_Node'Class;
      Predicate : access function (N : RFLX_Node) return Boolean := null)
      return RFLX_Node;
   --  Return the first node found under ``Root`` (included) that satisfies the
   --  given ``Predicate``. Return a null node if there is no such node.

   function Find_First
     (Root : RFLX_Node'Class; Predicate : RFLX_Node_Predicate'Class) return RFLX_Node;
   --  Return the first node found under ``Root`` (included) that satisfies the
   --  given ``Predicate``. Return a null node if there is no such node.

   ----------------
   -- Predicates --
   ----------------

   function Kind_Is (Kind : RFLX_Node_Kind_Type) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes of the given ``Kind``
   --
   --% belongs-to: RFLX_Node_Predicate

   function Kind_In (First, Last : RFLX_Node_Kind_Type) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes whose kind is in First ..
   --  Last.
   --
   --% belongs-to: RFLX_Node_Predicate

   function Text_Is (Text : Text_Type) return RFLX_Node_Predicate;
   --  Return a predicate that accepts only nodes that match the given ``Text``
   --
   --% belongs-to: RFLX_Node_Predicate

   function Node_Is_Null return RFLX_Node_Predicate;
   --  Return a predicate that accepts only null nodes
   --
   --% belongs-to: RFLX_Node_Predicate

   


private

   ------------------------
   -- Iterator internals --
   ------------------------

   function Get_Parent (N : RFLX_Node) return RFLX_Node;
   function First_Child_Index_For_Traverse (N : RFLX_Node) return Natural;
   function Last_Child_Index_For_Traverse (N : RFLX_Node) return Natural;
   function Get_Child (N : RFLX_Node; I : Natural) return RFLX_Node;

   package Traversal_Iterators is new Langkit_Support.Tree_Traversal_Iterator
     (Node_Type         => RFLX_Node,
      No_Node           => No_RFLX_Node,
      Node_Array        => RFLX_Node_Array,
      First_Child_Index => First_Child_Index_For_Traverse,
      Last_Child_Index  => Last_Child_Index_For_Traverse,
      Iterators         => RFLX_Node_Iterators);

   type Traverse_Iterator is
      new Traversal_Iterators.Traverse_Iterator with null record;

   type Find_Iterator is new Traverse_Iterator with record
      Predicate : RFLX_Node_Predicate;
      --  Predicate used to filter the nodes Traverse_It yields
   end record;
   --  Iterator type for the ``Find`` function

   overriding function Next
     (It : in out Find_Iterator; Element : out RFLX_Node) return Boolean;

   type Local_Find_Iterator is new Traverse_Iterator with record
      Predicate : access function (N : RFLX_Node) return Boolean;
      --  Predicate used to filter the nodes Traverse_It yields
   end record;
   --  Iterator type for the ``Find`` function that takes an access to
   --  function. It is called ``Local_Find_Iterator`` because if you use a
   --  locally declared function, the iterator itself will only be valid in the
   --  scope of the function.

   overriding function Next
     (It : in out Local_Find_Iterator; Element : out RFLX_Node) return Boolean;

   --------------------------
   -- Predicates internals --
   --------------------------

   type Not_Predicate is new RFLX_Node_Predicate_Interface with record
      Predicate : RFLX_Node_Predicate;
   end record;

   overriding function Evaluate
     (P : in out Not_Predicate; N : RFLX_Node) return Boolean;

   type For_All_Predicate (N : Natural) is new RFLX_Node_Predicate_Interface with record
      Predicates : RFLX_Node_Predicate_Array (1 .. N);
   end record;

   overriding function Evaluate
     (P : in out For_All_Predicate; N : RFLX_Node) return Boolean;

   type For_Some_Predicate (N : Natural) is new RFLX_Node_Predicate_Interface with record
      Predicates : RFLX_Node_Predicate_Array (1 .. N);
   end record;

   overriding function Evaluate
     (P : in out For_Some_Predicate; N : RFLX_Node) return Boolean;

   type For_All_Children_Predicate is new RFLX_Node_Predicate_Interface with record
      Predicate : RFLX_Node_Predicate;
      Skip_Null : Boolean;
   end record;

   overriding function Evaluate
     (P : in out For_All_Children_Predicate; N : RFLX_Node) return Boolean;

   type For_Some_Children_Predicate is new RFLX_Node_Predicate_Interface with record
      Predicate : RFLX_Node_Predicate;
      Skip_Null : Boolean;
   end record;

   overriding function Evaluate
     (P : in out For_Some_Children_Predicate; N : RFLX_Node) return Boolean;

   type Child_With_Predicate is new RFLX_Node_Predicate_Interface with record
      Field     : Syntax_Field_Reference;
      Predicate : RFLX_Node_Predicate;
   end record;

   overriding function Evaluate
     (P : in out Child_With_Predicate; N : RFLX_Node) return Boolean;

   type Kind_Predicate is new RFLX_Node_Predicate_Interface with record
      First, Last : RFLX_Node_Kind_Type;
   end record;
   --  Predicate that returns true for all nodes whose kind is in a given range

   overriding function Evaluate
     (P : in out Kind_Predicate; N : RFLX_Node) return Boolean;

   type Text_Predicate is new RFLX_Node_Predicate_Interface with record
      Text : Unbounded_Text_Type;
   end record;
   --  Predicate that returns true for all nodes that match some text

   overriding function Evaluate
     (P : in out Text_Predicate; N : RFLX_Node) return Boolean;

   type Node_Is_Null_Predicate is new RFLX_Node_Predicate_Interface with null record;

   overriding function Evaluate
     (P : in out Node_Is_Null_Predicate; N : RFLX_Node) return Boolean;

   


end Librflxlang.Iterators;
