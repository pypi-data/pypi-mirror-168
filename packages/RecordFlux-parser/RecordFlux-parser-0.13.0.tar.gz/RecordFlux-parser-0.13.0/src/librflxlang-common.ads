


with GNATCOLL.GMP.Integers;
with GNATCOLL.Traces;

with Langkit_Support.Errors;

with Langkit_Support.Symbols.Precomputed;
use Langkit_Support.Symbols;

with Langkit_Support.Token_Data_Handlers;
use Langkit_Support.Token_Data_Handlers;


--  This package provides types and functions used in the whole Librflxlang
--  package tree.

package Librflxlang.Common is

   use Support.Slocs, Support.Text;

   

   Main_Trace : constant GNATCOLL.Traces.Trace_Handle :=
     GNATCOLL.Traces.Create
       ("LIBRFLXLANG.MAIN_TRACE", GNATCOLL.Traces.From_Config);

   PLE_Errors_Trace : constant GNATCOLL.Traces.Trace_Handle :=
     GNATCOLL.Traces.Create
       ("LIBRFLXLANG.PLE_ERRORS", GNATCOLL.Traces.From_Config);

   Default_Charset : constant String := "utf-8";
   --  Default charset to use when creating analysis contexts

   subtype Big_Integer is GNATCOLL.GMP.Integers.Big_Integer;
   --  Shortcut for ``GNATCOLL.GMP.Integers.Big_Integer``

   -------------------------------------
   -- Symbols and token data handlers --
   -------------------------------------

   type Precomputed_Symbol_Index is
         new Integer range 1 .. 0
   ;

   function Precomputed_Symbol
     (Index : Precomputed_Symbol_Index) return Text_Type;

   --  GNAT emits an incorrect value not in range in instantiation warning...
   --  So deactivate them at the instantiation point.
   pragma Warnings (Off, "value not in range");
   package Precomputed_Symbols
   is new Langkit_Support.Symbols.Precomputed
     (Precomputed_Symbol_Index, Precomputed_Symbol);
   pragma Warnings (On, "value not in range");

   -----------
   -- Nodes --
   -----------

   type RFLX_Node_Kind_Type is
     (RFLX_ID, RFLX_UnqualifiedID, RFLX_Aspect, RFLX_Attr_First, RFLX_Attr_Has_Data, RFLX_Attr_Head, RFLX_Attr_Last, RFLX_Attr_Opaque, RFLX_Attr_Present, RFLX_Attr_Size, RFLX_Attr_Valid, RFLX_Attr_Valid_Checksum, RFLX_Attr_Stmt_Append, RFLX_Attr_Stmt_Extend, RFLX_Attr_Stmt_Read, RFLX_Attr_Stmt_Write, RFLX_Message_Aggregate_Associations, RFLX_Null_Message_Aggregate, RFLX_Checksum_Val, RFLX_Checksum_Value_Range, RFLX_Byte_Order_Type_Highorderfirst, RFLX_Byte_Order_Type_Loworderfirst, RFLX_Readable, RFLX_Writable, RFLX_Checksum_Assoc, RFLX_Refinement_Decl, RFLX_Session_Decl, RFLX_Type_Decl, RFLX_Description, RFLX_Element_Value_Assoc, RFLX_Attribute, RFLX_Bin_Op, RFLX_Binding, RFLX_Call, RFLX_Case_Expression, RFLX_Choice, RFLX_Comprehension, RFLX_Context_Item, RFLX_Conversion, RFLX_Message_Aggregate, RFLX_Negation, RFLX_Numeric_Literal, RFLX_Paren_Expression, RFLX_Quantified_Expression, RFLX_Select_Node, RFLX_Concatenation, RFLX_Sequence_Aggregate, RFLX_String_Literal, RFLX_Variable, RFLX_Formal_Channel_Decl, RFLX_Formal_Function_Decl, RFLX_Renaming_Decl, RFLX_Variable_Decl, RFLX_Message_Aggregate_Association, RFLX_Byte_Order_Aspect, RFLX_Checksum_Aspect, RFLX_Message_Field, RFLX_Message_Fields, RFLX_Null_Message_Field, RFLX_Op_Add, RFLX_Op_And, RFLX_Op_Div, RFLX_Op_Eq, RFLX_Op_Ge, RFLX_Op_Gt, RFLX_Op_In, RFLX_Op_Le, RFLX_Op_Lt, RFLX_Op_Mod, RFLX_Op_Mul, RFLX_Op_Neq, RFLX_Op_Notin, RFLX_Op_Or, RFLX_Op_Pow, RFLX_Op_Sub, RFLX_Package_Node, RFLX_Parameter, RFLX_Parameters, RFLX_Quantifier_All, RFLX_Quantifier_Some, RFLX_Aspect_List, RFLX_Base_Checksum_Val_List, RFLX_Channel_Attribute_List, RFLX_Checksum_Assoc_List, RFLX_Choice_List, RFLX_Conditional_Transition_List, RFLX_Context_Item_List, RFLX_Declaration_List, RFLX_Element_Value_Assoc_List, RFLX_Expr_List, RFLX_Formal_Decl_List, RFLX_Local_Decl_List, RFLX_Message_Aggregate_Association_List, RFLX_Message_Aspect_List, RFLX_Message_Field_List, RFLX_Numeric_Literal_List, RFLX_Parameter_List, RFLX_RFLX_Node_List, RFLX_State_List, RFLX_Statement_List, RFLX_Term_Assoc_List, RFLX_Then_Node_List, RFLX_Type_Argument_List, RFLX_UnqualifiedID_List, RFLX_Specification, RFLX_State, RFLX_State_Body, RFLX_Assignment, RFLX_Attribute_Statement, RFLX_Message_Field_Assignment, RFLX_Reset, RFLX_Term_Assoc, RFLX_Then_Node, RFLX_Transition, RFLX_Conditional_Transition, RFLX_Type_Argument, RFLX_Message_Type_Def, RFLX_Null_Message_Type_Def, RFLX_Named_Enumeration_Def, RFLX_Positional_Enumeration_Def, RFLX_Enumeration_Type_Def, RFLX_Modular_Type_Def, RFLX_Range_Type_Def, RFLX_Sequence_Type_Def, RFLX_Type_Derivation_Def);
   --  Type for concrete nodes

   for RFLX_Node_Kind_Type use
     (RFLX_ID => 1, RFLX_UnqualifiedID => 2, RFLX_Aspect => 3, RFLX_Attr_First => 4, RFLX_Attr_Has_Data => 5, RFLX_Attr_Head => 6, RFLX_Attr_Last => 7, RFLX_Attr_Opaque => 8, RFLX_Attr_Present => 9, RFLX_Attr_Size => 10, RFLX_Attr_Valid => 11, RFLX_Attr_Valid_Checksum => 12, RFLX_Attr_Stmt_Append => 13, RFLX_Attr_Stmt_Extend => 14, RFLX_Attr_Stmt_Read => 15, RFLX_Attr_Stmt_Write => 16, RFLX_Message_Aggregate_Associations => 17, RFLX_Null_Message_Aggregate => 18, RFLX_Checksum_Val => 19, RFLX_Checksum_Value_Range => 20, RFLX_Byte_Order_Type_Highorderfirst => 21, RFLX_Byte_Order_Type_Loworderfirst => 22, RFLX_Readable => 23, RFLX_Writable => 24, RFLX_Checksum_Assoc => 25, RFLX_Refinement_Decl => 26, RFLX_Session_Decl => 27, RFLX_Type_Decl => 28, RFLX_Description => 29, RFLX_Element_Value_Assoc => 30, RFLX_Attribute => 31, RFLX_Bin_Op => 32, RFLX_Binding => 33, RFLX_Call => 34, RFLX_Case_Expression => 35, RFLX_Choice => 36, RFLX_Comprehension => 37, RFLX_Context_Item => 38, RFLX_Conversion => 39, RFLX_Message_Aggregate => 40, RFLX_Negation => 41, RFLX_Numeric_Literal => 42, RFLX_Paren_Expression => 43, RFLX_Quantified_Expression => 44, RFLX_Select_Node => 45, RFLX_Concatenation => 46, RFLX_Sequence_Aggregate => 47, RFLX_String_Literal => 48, RFLX_Variable => 49, RFLX_Formal_Channel_Decl => 50, RFLX_Formal_Function_Decl => 51, RFLX_Renaming_Decl => 52, RFLX_Variable_Decl => 53, RFLX_Message_Aggregate_Association => 54, RFLX_Byte_Order_Aspect => 55, RFLX_Checksum_Aspect => 56, RFLX_Message_Field => 57, RFLX_Message_Fields => 58, RFLX_Null_Message_Field => 59, RFLX_Op_Add => 60, RFLX_Op_And => 61, RFLX_Op_Div => 62, RFLX_Op_Eq => 63, RFLX_Op_Ge => 64, RFLX_Op_Gt => 65, RFLX_Op_In => 66, RFLX_Op_Le => 67, RFLX_Op_Lt => 68, RFLX_Op_Mod => 69, RFLX_Op_Mul => 70, RFLX_Op_Neq => 71, RFLX_Op_Notin => 72, RFLX_Op_Or => 73, RFLX_Op_Pow => 74, RFLX_Op_Sub => 75, RFLX_Package_Node => 76, RFLX_Parameter => 77, RFLX_Parameters => 78, RFLX_Quantifier_All => 79, RFLX_Quantifier_Some => 80, RFLX_Aspect_List => 81, RFLX_Base_Checksum_Val_List => 82, RFLX_Channel_Attribute_List => 83, RFLX_Checksum_Assoc_List => 84, RFLX_Choice_List => 85, RFLX_Conditional_Transition_List => 86, RFLX_Context_Item_List => 87, RFLX_Declaration_List => 88, RFLX_Element_Value_Assoc_List => 89, RFLX_Expr_List => 90, RFLX_Formal_Decl_List => 91, RFLX_Local_Decl_List => 92, RFLX_Message_Aggregate_Association_List => 93, RFLX_Message_Aspect_List => 94, RFLX_Message_Field_List => 95, RFLX_Numeric_Literal_List => 96, RFLX_Parameter_List => 97, RFLX_RFLX_Node_List => 98, RFLX_State_List => 99, RFLX_Statement_List => 100, RFLX_Term_Assoc_List => 101, RFLX_Then_Node_List => 102, RFLX_Type_Argument_List => 103, RFLX_UnqualifiedID_List => 104, RFLX_Specification => 105, RFLX_State => 106, RFLX_State_Body => 107, RFLX_Assignment => 108, RFLX_Attribute_Statement => 109, RFLX_Message_Field_Assignment => 110, RFLX_Reset => 111, RFLX_Term_Assoc => 112, RFLX_Then_Node => 113, RFLX_Transition => 114, RFLX_Conditional_Transition => 115, RFLX_Type_Argument => 116, RFLX_Message_Type_Def => 117, RFLX_Null_Message_Type_Def => 118, RFLX_Named_Enumeration_Def => 119, RFLX_Positional_Enumeration_Def => 120, RFLX_Enumeration_Type_Def => 121, RFLX_Modular_Type_Def => 122, RFLX_Range_Type_Def => 123, RFLX_Sequence_Type_Def => 124, RFLX_Type_Derivation_Def => 125);

      subtype RFLX_RFLX_Node is RFLX_Node_Kind_Type
            range RFLX_ID .. RFLX_Type_Derivation_Def;
      --% no-document: True
      subtype RFLX_AbstractID is RFLX_Node_Kind_Type
            range RFLX_ID .. RFLX_UnqualifiedID;
      --% no-document: True
      subtype RFLX_ID_Range is RFLX_Node_Kind_Type
            range RFLX_ID .. RFLX_ID;
      --% no-document: True
      subtype RFLX_UnqualifiedID_Range is RFLX_Node_Kind_Type
            range RFLX_UnqualifiedID .. RFLX_UnqualifiedID;
      --% no-document: True
      subtype RFLX_Aspect_Range is RFLX_Node_Kind_Type
            range RFLX_Aspect .. RFLX_Aspect;
      --% no-document: True
      subtype RFLX_Attr is RFLX_Node_Kind_Type
            range RFLX_Attr_First .. RFLX_Attr_Valid_Checksum;
      --% no-document: True
      subtype RFLX_Attr_First_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_First .. RFLX_Attr_First;
      --% no-document: True
      subtype RFLX_Attr_Has_Data_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Has_Data .. RFLX_Attr_Has_Data;
      --% no-document: True
      subtype RFLX_Attr_Head_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Head .. RFLX_Attr_Head;
      --% no-document: True
      subtype RFLX_Attr_Last_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Last .. RFLX_Attr_Last;
      --% no-document: True
      subtype RFLX_Attr_Opaque_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Opaque .. RFLX_Attr_Opaque;
      --% no-document: True
      subtype RFLX_Attr_Present_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Present .. RFLX_Attr_Present;
      --% no-document: True
      subtype RFLX_Attr_Size_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Size .. RFLX_Attr_Size;
      --% no-document: True
      subtype RFLX_Attr_Valid_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Valid .. RFLX_Attr_Valid;
      --% no-document: True
      subtype RFLX_Attr_Valid_Checksum_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Valid_Checksum .. RFLX_Attr_Valid_Checksum;
      --% no-document: True
      subtype RFLX_Attr_Stmt is RFLX_Node_Kind_Type
            range RFLX_Attr_Stmt_Append .. RFLX_Attr_Stmt_Write;
      --% no-document: True
      subtype RFLX_Attr_Stmt_Append_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Stmt_Append .. RFLX_Attr_Stmt_Append;
      --% no-document: True
      subtype RFLX_Attr_Stmt_Extend_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Stmt_Extend .. RFLX_Attr_Stmt_Extend;
      --% no-document: True
      subtype RFLX_Attr_Stmt_Read_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Stmt_Read .. RFLX_Attr_Stmt_Read;
      --% no-document: True
      subtype RFLX_Attr_Stmt_Write_Range is RFLX_Node_Kind_Type
            range RFLX_Attr_Stmt_Write .. RFLX_Attr_Stmt_Write;
      --% no-document: True
      subtype RFLX_Base_Aggregate is RFLX_Node_Kind_Type
            range RFLX_Message_Aggregate_Associations .. RFLX_Null_Message_Aggregate;
      --% no-document: True
      subtype RFLX_Message_Aggregate_Associations_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Aggregate_Associations .. RFLX_Message_Aggregate_Associations;
      --% no-document: True
      subtype RFLX_Null_Message_Aggregate_Range is RFLX_Node_Kind_Type
            range RFLX_Null_Message_Aggregate .. RFLX_Null_Message_Aggregate;
      --% no-document: True
      subtype RFLX_Base_Checksum_Val is RFLX_Node_Kind_Type
            range RFLX_Checksum_Val .. RFLX_Checksum_Value_Range;
      --% no-document: True
      subtype RFLX_Checksum_Val_Range is RFLX_Node_Kind_Type
            range RFLX_Checksum_Val .. RFLX_Checksum_Val;
      --% no-document: True
      subtype RFLX_Checksum_Value_Range_Range is RFLX_Node_Kind_Type
            range RFLX_Checksum_Value_Range .. RFLX_Checksum_Value_Range;
      --% no-document: True
      subtype RFLX_Byte_Order_Type is RFLX_Node_Kind_Type
            range RFLX_Byte_Order_Type_Highorderfirst .. RFLX_Byte_Order_Type_Loworderfirst;
      --% no-document: True
      subtype RFLX_Byte_Order_Type_Highorderfirst_Range is RFLX_Node_Kind_Type
            range RFLX_Byte_Order_Type_Highorderfirst .. RFLX_Byte_Order_Type_Highorderfirst;
      --% no-document: True
      subtype RFLX_Byte_Order_Type_Loworderfirst_Range is RFLX_Node_Kind_Type
            range RFLX_Byte_Order_Type_Loworderfirst .. RFLX_Byte_Order_Type_Loworderfirst;
      --% no-document: True
      subtype RFLX_Channel_Attribute is RFLX_Node_Kind_Type
            range RFLX_Readable .. RFLX_Writable;
      --% no-document: True
      subtype RFLX_Readable_Range is RFLX_Node_Kind_Type
            range RFLX_Readable .. RFLX_Readable;
      --% no-document: True
      subtype RFLX_Writable_Range is RFLX_Node_Kind_Type
            range RFLX_Writable .. RFLX_Writable;
      --% no-document: True
      subtype RFLX_Checksum_Assoc_Range is RFLX_Node_Kind_Type
            range RFLX_Checksum_Assoc .. RFLX_Checksum_Assoc;
      --% no-document: True
      subtype RFLX_Declaration is RFLX_Node_Kind_Type
            range RFLX_Refinement_Decl .. RFLX_Type_Decl;
      --% no-document: True
      subtype RFLX_Refinement_Decl_Range is RFLX_Node_Kind_Type
            range RFLX_Refinement_Decl .. RFLX_Refinement_Decl;
      --% no-document: True
      subtype RFLX_Session_Decl_Range is RFLX_Node_Kind_Type
            range RFLX_Session_Decl .. RFLX_Session_Decl;
      --% no-document: True
      subtype RFLX_Type_Decl_Range is RFLX_Node_Kind_Type
            range RFLX_Type_Decl .. RFLX_Type_Decl;
      --% no-document: True
      subtype RFLX_Description_Range is RFLX_Node_Kind_Type
            range RFLX_Description .. RFLX_Description;
      --% no-document: True
      subtype RFLX_Element_Value_Assoc_Range is RFLX_Node_Kind_Type
            range RFLX_Element_Value_Assoc .. RFLX_Element_Value_Assoc;
      --% no-document: True
      subtype RFLX_Expr is RFLX_Node_Kind_Type
            range RFLX_Attribute .. RFLX_Variable;
      --% no-document: True
      subtype RFLX_Attribute_Range is RFLX_Node_Kind_Type
            range RFLX_Attribute .. RFLX_Attribute;
      --% no-document: True
      subtype RFLX_Bin_Op_Range is RFLX_Node_Kind_Type
            range RFLX_Bin_Op .. RFLX_Bin_Op;
      --% no-document: True
      subtype RFLX_Binding_Range is RFLX_Node_Kind_Type
            range RFLX_Binding .. RFLX_Binding;
      --% no-document: True
      subtype RFLX_Call_Range is RFLX_Node_Kind_Type
            range RFLX_Call .. RFLX_Call;
      --% no-document: True
      subtype RFLX_Case_Expression_Range is RFLX_Node_Kind_Type
            range RFLX_Case_Expression .. RFLX_Case_Expression;
      --% no-document: True
      subtype RFLX_Choice_Range is RFLX_Node_Kind_Type
            range RFLX_Choice .. RFLX_Choice;
      --% no-document: True
      subtype RFLX_Comprehension_Range is RFLX_Node_Kind_Type
            range RFLX_Comprehension .. RFLX_Comprehension;
      --% no-document: True
      subtype RFLX_Context_Item_Range is RFLX_Node_Kind_Type
            range RFLX_Context_Item .. RFLX_Context_Item;
      --% no-document: True
      subtype RFLX_Conversion_Range is RFLX_Node_Kind_Type
            range RFLX_Conversion .. RFLX_Conversion;
      --% no-document: True
      subtype RFLX_Message_Aggregate_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Aggregate .. RFLX_Message_Aggregate;
      --% no-document: True
      subtype RFLX_Negation_Range is RFLX_Node_Kind_Type
            range RFLX_Negation .. RFLX_Negation;
      --% no-document: True
      subtype RFLX_Numeric_Literal_Range is RFLX_Node_Kind_Type
            range RFLX_Numeric_Literal .. RFLX_Numeric_Literal;
      --% no-document: True
      subtype RFLX_Paren_Expression_Range is RFLX_Node_Kind_Type
            range RFLX_Paren_Expression .. RFLX_Paren_Expression;
      --% no-document: True
      subtype RFLX_Quantified_Expression_Range is RFLX_Node_Kind_Type
            range RFLX_Quantified_Expression .. RFLX_Quantified_Expression;
      --% no-document: True
      subtype RFLX_Select_Node_Range is RFLX_Node_Kind_Type
            range RFLX_Select_Node .. RFLX_Select_Node;
      --% no-document: True
      subtype RFLX_Sequence_Literal is RFLX_Node_Kind_Type
            range RFLX_Concatenation .. RFLX_String_Literal;
      --% no-document: True
      subtype RFLX_Concatenation_Range is RFLX_Node_Kind_Type
            range RFLX_Concatenation .. RFLX_Concatenation;
      --% no-document: True
      subtype RFLX_Sequence_Aggregate_Range is RFLX_Node_Kind_Type
            range RFLX_Sequence_Aggregate .. RFLX_Sequence_Aggregate;
      --% no-document: True
      subtype RFLX_String_Literal_Range is RFLX_Node_Kind_Type
            range RFLX_String_Literal .. RFLX_String_Literal;
      --% no-document: True
      subtype RFLX_Variable_Range is RFLX_Node_Kind_Type
            range RFLX_Variable .. RFLX_Variable;
      --% no-document: True
      subtype RFLX_Formal_Decl is RFLX_Node_Kind_Type
            range RFLX_Formal_Channel_Decl .. RFLX_Formal_Function_Decl;
      --% no-document: True
      subtype RFLX_Formal_Channel_Decl_Range is RFLX_Node_Kind_Type
            range RFLX_Formal_Channel_Decl .. RFLX_Formal_Channel_Decl;
      --% no-document: True
      subtype RFLX_Formal_Function_Decl_Range is RFLX_Node_Kind_Type
            range RFLX_Formal_Function_Decl .. RFLX_Formal_Function_Decl;
      --% no-document: True
      subtype RFLX_Local_Decl is RFLX_Node_Kind_Type
            range RFLX_Renaming_Decl .. RFLX_Variable_Decl;
      --% no-document: True
      subtype RFLX_Renaming_Decl_Range is RFLX_Node_Kind_Type
            range RFLX_Renaming_Decl .. RFLX_Renaming_Decl;
      --% no-document: True
      subtype RFLX_Variable_Decl_Range is RFLX_Node_Kind_Type
            range RFLX_Variable_Decl .. RFLX_Variable_Decl;
      --% no-document: True
      subtype RFLX_Message_Aggregate_Association_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Aggregate_Association .. RFLX_Message_Aggregate_Association;
      --% no-document: True
      subtype RFLX_Message_Aspect is RFLX_Node_Kind_Type
            range RFLX_Byte_Order_Aspect .. RFLX_Checksum_Aspect;
      --% no-document: True
      subtype RFLX_Byte_Order_Aspect_Range is RFLX_Node_Kind_Type
            range RFLX_Byte_Order_Aspect .. RFLX_Byte_Order_Aspect;
      --% no-document: True
      subtype RFLX_Checksum_Aspect_Range is RFLX_Node_Kind_Type
            range RFLX_Checksum_Aspect .. RFLX_Checksum_Aspect;
      --% no-document: True
      subtype RFLX_Message_Field_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Field .. RFLX_Message_Field;
      --% no-document: True
      subtype RFLX_Message_Fields_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Fields .. RFLX_Message_Fields;
      --% no-document: True
      subtype RFLX_Null_Message_Field_Range is RFLX_Node_Kind_Type
            range RFLX_Null_Message_Field .. RFLX_Null_Message_Field;
      --% no-document: True
      subtype RFLX_Op is RFLX_Node_Kind_Type
            range RFLX_Op_Add .. RFLX_Op_Sub;
      --% no-document: True
      subtype RFLX_Op_Add_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Add .. RFLX_Op_Add;
      --% no-document: True
      subtype RFLX_Op_And_Range is RFLX_Node_Kind_Type
            range RFLX_Op_And .. RFLX_Op_And;
      --% no-document: True
      subtype RFLX_Op_Div_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Div .. RFLX_Op_Div;
      --% no-document: True
      subtype RFLX_Op_Eq_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Eq .. RFLX_Op_Eq;
      --% no-document: True
      subtype RFLX_Op_Ge_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Ge .. RFLX_Op_Ge;
      --% no-document: True
      subtype RFLX_Op_Gt_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Gt .. RFLX_Op_Gt;
      --% no-document: True
      subtype RFLX_Op_In_Range is RFLX_Node_Kind_Type
            range RFLX_Op_In .. RFLX_Op_In;
      --% no-document: True
      subtype RFLX_Op_Le_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Le .. RFLX_Op_Le;
      --% no-document: True
      subtype RFLX_Op_Lt_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Lt .. RFLX_Op_Lt;
      --% no-document: True
      subtype RFLX_Op_Mod_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Mod .. RFLX_Op_Mod;
      --% no-document: True
      subtype RFLX_Op_Mul_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Mul .. RFLX_Op_Mul;
      --% no-document: True
      subtype RFLX_Op_Neq_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Neq .. RFLX_Op_Neq;
      --% no-document: True
      subtype RFLX_Op_Notin_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Notin .. RFLX_Op_Notin;
      --% no-document: True
      subtype RFLX_Op_Or_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Or .. RFLX_Op_Or;
      --% no-document: True
      subtype RFLX_Op_Pow_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Pow .. RFLX_Op_Pow;
      --% no-document: True
      subtype RFLX_Op_Sub_Range is RFLX_Node_Kind_Type
            range RFLX_Op_Sub .. RFLX_Op_Sub;
      --% no-document: True
      subtype RFLX_Package_Node_Range is RFLX_Node_Kind_Type
            range RFLX_Package_Node .. RFLX_Package_Node;
      --% no-document: True
      subtype RFLX_Parameter_Range is RFLX_Node_Kind_Type
            range RFLX_Parameter .. RFLX_Parameter;
      --% no-document: True
      subtype RFLX_Parameters_Range is RFLX_Node_Kind_Type
            range RFLX_Parameters .. RFLX_Parameters;
      --% no-document: True
      subtype RFLX_Quantifier is RFLX_Node_Kind_Type
            range RFLX_Quantifier_All .. RFLX_Quantifier_Some;
      --% no-document: True
      subtype RFLX_Quantifier_All_Range is RFLX_Node_Kind_Type
            range RFLX_Quantifier_All .. RFLX_Quantifier_All;
      --% no-document: True
      subtype RFLX_Quantifier_Some_Range is RFLX_Node_Kind_Type
            range RFLX_Quantifier_Some .. RFLX_Quantifier_Some;
      --% no-document: True
      subtype RFLX_RFLX_Node_Base_List is RFLX_Node_Kind_Type
            range RFLX_Aspect_List .. RFLX_UnqualifiedID_List;
      --% no-document: True
      subtype RFLX_Aspect_List_Range is RFLX_Node_Kind_Type
            range RFLX_Aspect_List .. RFLX_Aspect_List;
      --% no-document: True
      subtype RFLX_Base_Checksum_Val_List_Range is RFLX_Node_Kind_Type
            range RFLX_Base_Checksum_Val_List .. RFLX_Base_Checksum_Val_List;
      --% no-document: True
      subtype RFLX_Channel_Attribute_List_Range is RFLX_Node_Kind_Type
            range RFLX_Channel_Attribute_List .. RFLX_Channel_Attribute_List;
      --% no-document: True
      subtype RFLX_Checksum_Assoc_List_Range is RFLX_Node_Kind_Type
            range RFLX_Checksum_Assoc_List .. RFLX_Checksum_Assoc_List;
      --% no-document: True
      subtype RFLX_Choice_List_Range is RFLX_Node_Kind_Type
            range RFLX_Choice_List .. RFLX_Choice_List;
      --% no-document: True
      subtype RFLX_Conditional_Transition_List_Range is RFLX_Node_Kind_Type
            range RFLX_Conditional_Transition_List .. RFLX_Conditional_Transition_List;
      --% no-document: True
      subtype RFLX_Context_Item_List_Range is RFLX_Node_Kind_Type
            range RFLX_Context_Item_List .. RFLX_Context_Item_List;
      --% no-document: True
      subtype RFLX_Declaration_List_Range is RFLX_Node_Kind_Type
            range RFLX_Declaration_List .. RFLX_Declaration_List;
      --% no-document: True
      subtype RFLX_Element_Value_Assoc_List_Range is RFLX_Node_Kind_Type
            range RFLX_Element_Value_Assoc_List .. RFLX_Element_Value_Assoc_List;
      --% no-document: True
      subtype RFLX_Expr_List_Range is RFLX_Node_Kind_Type
            range RFLX_Expr_List .. RFLX_Expr_List;
      --% no-document: True
      subtype RFLX_Formal_Decl_List_Range is RFLX_Node_Kind_Type
            range RFLX_Formal_Decl_List .. RFLX_Formal_Decl_List;
      --% no-document: True
      subtype RFLX_Local_Decl_List_Range is RFLX_Node_Kind_Type
            range RFLX_Local_Decl_List .. RFLX_Local_Decl_List;
      --% no-document: True
      subtype RFLX_Message_Aggregate_Association_List_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Aggregate_Association_List .. RFLX_Message_Aggregate_Association_List;
      --% no-document: True
      subtype RFLX_Message_Aspect_List_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Aspect_List .. RFLX_Message_Aspect_List;
      --% no-document: True
      subtype RFLX_Message_Field_List_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Field_List .. RFLX_Message_Field_List;
      --% no-document: True
      subtype RFLX_Numeric_Literal_List_Range is RFLX_Node_Kind_Type
            range RFLX_Numeric_Literal_List .. RFLX_Numeric_Literal_List;
      --% no-document: True
      subtype RFLX_Parameter_List_Range is RFLX_Node_Kind_Type
            range RFLX_Parameter_List .. RFLX_Parameter_List;
      --% no-document: True
      subtype RFLX_RFLX_Node_List_Range is RFLX_Node_Kind_Type
            range RFLX_RFLX_Node_List .. RFLX_RFLX_Node_List;
      --% no-document: True
      subtype RFLX_State_List_Range is RFLX_Node_Kind_Type
            range RFLX_State_List .. RFLX_State_List;
      --% no-document: True
      subtype RFLX_Statement_List_Range is RFLX_Node_Kind_Type
            range RFLX_Statement_List .. RFLX_Statement_List;
      --% no-document: True
      subtype RFLX_Term_Assoc_List_Range is RFLX_Node_Kind_Type
            range RFLX_Term_Assoc_List .. RFLX_Term_Assoc_List;
      --% no-document: True
      subtype RFLX_Then_Node_List_Range is RFLX_Node_Kind_Type
            range RFLX_Then_Node_List .. RFLX_Then_Node_List;
      --% no-document: True
      subtype RFLX_Type_Argument_List_Range is RFLX_Node_Kind_Type
            range RFLX_Type_Argument_List .. RFLX_Type_Argument_List;
      --% no-document: True
      subtype RFLX_UnqualifiedID_List_Range is RFLX_Node_Kind_Type
            range RFLX_UnqualifiedID_List .. RFLX_UnqualifiedID_List;
      --% no-document: True
      subtype RFLX_Specification_Range is RFLX_Node_Kind_Type
            range RFLX_Specification .. RFLX_Specification;
      --% no-document: True
      subtype RFLX_State_Range is RFLX_Node_Kind_Type
            range RFLX_State .. RFLX_State;
      --% no-document: True
      subtype RFLX_State_Body_Range is RFLX_Node_Kind_Type
            range RFLX_State_Body .. RFLX_State_Body;
      --% no-document: True
      subtype RFLX_Statement is RFLX_Node_Kind_Type
            range RFLX_Assignment .. RFLX_Reset;
      --% no-document: True
      subtype RFLX_Assignment_Range is RFLX_Node_Kind_Type
            range RFLX_Assignment .. RFLX_Assignment;
      --% no-document: True
      subtype RFLX_Attribute_Statement_Range is RFLX_Node_Kind_Type
            range RFLX_Attribute_Statement .. RFLX_Attribute_Statement;
      --% no-document: True
      subtype RFLX_Message_Field_Assignment_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Field_Assignment .. RFLX_Message_Field_Assignment;
      --% no-document: True
      subtype RFLX_Reset_Range is RFLX_Node_Kind_Type
            range RFLX_Reset .. RFLX_Reset;
      --% no-document: True
      subtype RFLX_Term_Assoc_Range is RFLX_Node_Kind_Type
            range RFLX_Term_Assoc .. RFLX_Term_Assoc;
      --% no-document: True
      subtype RFLX_Then_Node_Range is RFLX_Node_Kind_Type
            range RFLX_Then_Node .. RFLX_Then_Node;
      --% no-document: True
      subtype RFLX_Transition_Range is RFLX_Node_Kind_Type
            range RFLX_Transition .. RFLX_Conditional_Transition;
      --% no-document: True
      subtype RFLX_Conditional_Transition_Range is RFLX_Node_Kind_Type
            range RFLX_Conditional_Transition .. RFLX_Conditional_Transition;
      --% no-document: True
      subtype RFLX_Type_Argument_Range is RFLX_Node_Kind_Type
            range RFLX_Type_Argument .. RFLX_Type_Argument;
      --% no-document: True
      subtype RFLX_Type_Def is RFLX_Node_Kind_Type
            range RFLX_Message_Type_Def .. RFLX_Type_Derivation_Def;
      --% no-document: True
      subtype RFLX_Abstract_Message_Type_Def is RFLX_Node_Kind_Type
            range RFLX_Message_Type_Def .. RFLX_Null_Message_Type_Def;
      --% no-document: True
      subtype RFLX_Message_Type_Def_Range is RFLX_Node_Kind_Type
            range RFLX_Message_Type_Def .. RFLX_Message_Type_Def;
      --% no-document: True
      subtype RFLX_Null_Message_Type_Def_Range is RFLX_Node_Kind_Type
            range RFLX_Null_Message_Type_Def .. RFLX_Null_Message_Type_Def;
      --% no-document: True
      subtype RFLX_Enumeration_Def is RFLX_Node_Kind_Type
            range RFLX_Named_Enumeration_Def .. RFLX_Positional_Enumeration_Def;
      --% no-document: True
      subtype RFLX_Named_Enumeration_Def_Range is RFLX_Node_Kind_Type
            range RFLX_Named_Enumeration_Def .. RFLX_Named_Enumeration_Def;
      --% no-document: True
      subtype RFLX_Positional_Enumeration_Def_Range is RFLX_Node_Kind_Type
            range RFLX_Positional_Enumeration_Def .. RFLX_Positional_Enumeration_Def;
      --% no-document: True
      subtype RFLX_Enumeration_Type_Def_Range is RFLX_Node_Kind_Type
            range RFLX_Enumeration_Type_Def .. RFLX_Enumeration_Type_Def;
      --% no-document: True
      subtype RFLX_Integer_Type_Def is RFLX_Node_Kind_Type
            range RFLX_Modular_Type_Def .. RFLX_Range_Type_Def;
      --% no-document: True
      subtype RFLX_Modular_Type_Def_Range is RFLX_Node_Kind_Type
            range RFLX_Modular_Type_Def .. RFLX_Modular_Type_Def;
      --% no-document: True
      subtype RFLX_Range_Type_Def_Range is RFLX_Node_Kind_Type
            range RFLX_Range_Type_Def .. RFLX_Range_Type_Def;
      --% no-document: True
      subtype RFLX_Sequence_Type_Def_Range is RFLX_Node_Kind_Type
            range RFLX_Sequence_Type_Def .. RFLX_Sequence_Type_Def;
      --% no-document: True
      subtype RFLX_Type_Derivation_Def_Range is RFLX_Node_Kind_Type
            range RFLX_Type_Derivation_Def .. RFLX_Type_Derivation_Def;
      --% no-document: True

   subtype Synthetic_Nodes is RFLX_Node_Kind_Type
      with Static_Predicate =>
         False
   ;
   --  Set of nodes that are synthetic.
      --
      --  Parsers cannot create synthetic nodes, so these correspond to no
      --  source text. These nodes are created dynamically for convenience
      --  during semantic analysis.

      type Analysis_Unit_Kind is
        (Unit_Specification, Unit_Body)
         with Convention => C;
      --  Specify a kind of analysis unit. Specification units provide an
      --  interface to the outer world while body units provide an
      --  implementation for the corresponding interface.


      function Trace_Image (Self : Analysis_Unit_Kind) return String
      is (Self'Image);

      type Lookup_Kind is
        (Recursive, Flat, Minimal)
         with Convention => C;
      


      function Trace_Image (Self : Lookup_Kind) return String
      is (Self'Image);

      type Grammar_Rule is
        (Main_Rule_Rule, Unqualified_Identifier_Rule, Qualified_Identifier_Rule, Numeric_Literal_Rule, Variable_Rule, Sequence_Aggregate_Rule, String_Literal_Rule, Concatenation_Rule, Primary_Rule, Paren_Expression_Rule, Suffix_Rule, Factor_Rule, Term_Rule, Unop_Term_Rule, Simple_Expr_Rule, Relation_Rule, Expression_Rule, Quantified_Expression_Rule, Comprehension_Rule, Call_Rule, Conversion_Rule, Null_Message_Aggregate_Rule, Message_Aggregate_Association_Rule, Message_Aggregate_Association_List_Rule, Message_Aggregate_Rule, Extended_Primary_Rule, Extended_Paren_Expression_Rule, Extended_Choice_List_Rule, Extended_Choices_Rule, Extended_Case_Expression_Rule, Extended_Suffix_Rule, Extended_Factor_Rule, Extended_Term_Rule, Extended_Unop_Term_Rule, Extended_Simple_Expr_Rule, Extended_Relation_Rule, Extended_Expression_Rule, Aspect_Rule, Range_Type_Definition_Rule, Modular_Type_Definition_Rule, Integer_Type_Definition_Rule, If_Condition_Rule, Extended_If_Condition_Rule, Then_Rule, Type_Argument_Rule, Null_Message_Field_Rule, Message_Field_Rule, Message_Field_List_Rule, Value_Range_Rule, Checksum_Association_Rule, Checksum_Aspect_Rule, Byte_Order_Aspect_Rule, Message_Aspect_List_Rule, Message_Type_Definition_Rule, Positional_Enumeration_Rule, Element_Value_Association_Rule, Named_Enumeration_Rule, Enumeration_Aspects_Rule, Enumeration_Type_Definition_Rule, Type_Derivation_Definition_Rule, Sequence_Type_Definition_Rule, Type_Declaration_Rule, Type_Refinement_Rule, Parameter_Rule, Parameter_List_Rule, Formal_Function_Declaration_Rule, Channel_Declaration_Rule, Session_Parameter_Rule, Renaming_Declaration_Rule, Variable_Declaration_Rule, Declaration_Rule, Description_Aspect_Rule, Assignment_Statement_Rule, Message_Field_Assignment_Statement_Rule, List_Attribute_Rule, Reset_Rule, Attribute_Statement_Rule, Action_Rule, Conditional_Transition_Rule, Transition_Rule, State_Body_Rule, State_Rule, Session_Declaration_Rule, Basic_Declaration_Rule, Basic_Declarations_Rule, Package_Declaration_Rule, Context_Item_Rule, Context_Clause_Rule, Specification_Rule)
         with Convention => C;
      --  Gramar rule to use for parsing.


      function Trace_Image (Self : Grammar_Rule) return String
      is (Self'Image);


   Default_Grammar_Rule : constant Grammar_Rule := Main_Rule_Rule;
   --  Default grammar rule to use when parsing analysis units

   type Lexer_Input_Kind is
     (File,
      --  Readable source file

      Bytes_Buffer,
      --  Buffer of undecoded bytes

      Text_Buffer
      --  Buffer of decoded bytes
   );
   --  Kind of lexer input

   subtype Undecoded_Lexer_Input is
      Lexer_Input_Kind range File ..  Bytes_Buffer;

   type Token_Kind is (
      RFLX_Termination,
RFLX_Lexing_Failure,
RFLX_Unqualified_Identifier,
RFLX_Package,
RFLX_Is,
RFLX_If,
RFLX_End,
RFLX_Null,
RFLX_Type,
RFLX_Range,
RFLX_With,
RFLX_Mod,
RFLX_Message,
RFLX_Then,
RFLX_Sequence,
RFLX_Of,
RFLX_In,
RFLX_Not,
RFLX_New,
RFLX_For,
RFLX_When,
RFLX_Where,
RFLX_Use,
RFLX_All,
RFLX_Some,
RFLX_Generic,
RFLX_Session,
RFLX_Begin,
RFLX_Return,
RFLX_Function,
RFLX_State,
RFLX_Transition,
RFLX_Goto,
RFLX_Exception,
RFLX_Renames,
RFLX_Channel,
RFLX_Readable,
RFLX_Writable,
RFLX_Desc,
RFLX_Append,
RFLX_Extend,
RFLX_Read,
RFLX_Write,
RFLX_Reset,
RFLX_High_Order_First,
RFLX_Low_Order_First,
RFLX_Case,
RFLX_First,
RFLX_Size,
RFLX_Last,
RFLX_Byte_Order,
RFLX_Checksum,
RFLX_Valid_Checksum,
RFLX_Has_Data,
RFLX_Head,
RFLX_Opaque,
RFLX_Present,
RFLX_Valid,
RFLX_Dot,
RFLX_Comma,
RFLX_Double_Dot,
RFLX_Tick,
RFLX_Hash,
RFLX_Minus,
RFLX_Arrow,
RFLX_L_Par,
RFLX_R_Par,
RFLX_L_Brack,
RFLX_R_Brack,
RFLX_Exp,
RFLX_Mul,
RFLX_Div,
RFLX_Add,
RFLX_Sub,
RFLX_Eq,
RFLX_Neq,
RFLX_Leq,
RFLX_Lt,
RFLX_Le,
RFLX_Gt,
RFLX_Ge,
RFLX_And,
RFLX_Or,
RFLX_Ampersand,
RFLX_Semicolon,
RFLX_Double_Colon,
RFLX_Assignment,
RFLX_Colon,
RFLX_Pipe,
RFLX_Comment,
RFLX_Numeral,
RFLX_String_Literal
   );
   --  Kind of token: indentifier, string literal, ...

   type Token_Family is
     (Default_Family);
   --  Groups of token kinds, to make the processing of some groups of token
   --  uniform.


   Token_Kind_To_Family : array (Token_Kind) of Token_Family :=
     (RFLX_Termination => Default_Family, RFLX_Lexing_Failure => Default_Family, RFLX_Unqualified_Identifier => Default_Family, RFLX_Package => Default_Family, RFLX_Is => Default_Family, RFLX_If => Default_Family, RFLX_End => Default_Family, RFLX_Null => Default_Family, RFLX_Type => Default_Family, RFLX_Range => Default_Family, RFLX_With => Default_Family, RFLX_Mod => Default_Family, RFLX_Message => Default_Family, RFLX_Then => Default_Family, RFLX_Sequence => Default_Family, RFLX_Of => Default_Family, RFLX_In => Default_Family, RFLX_Not => Default_Family, RFLX_New => Default_Family, RFLX_For => Default_Family, RFLX_When => Default_Family, RFLX_Where => Default_Family, RFLX_Use => Default_Family, RFLX_All => Default_Family, RFLX_Some => Default_Family, RFLX_Generic => Default_Family, RFLX_Session => Default_Family, RFLX_Begin => Default_Family, RFLX_Return => Default_Family, RFLX_Function => Default_Family, RFLX_State => Default_Family, RFLX_Transition => Default_Family, RFLX_Goto => Default_Family, RFLX_Exception => Default_Family, RFLX_Renames => Default_Family, RFLX_Channel => Default_Family, RFLX_Readable => Default_Family, RFLX_Writable => Default_Family, RFLX_Desc => Default_Family, RFLX_Append => Default_Family, RFLX_Extend => Default_Family, RFLX_Read => Default_Family, RFLX_Write => Default_Family, RFLX_Reset => Default_Family, RFLX_High_Order_First => Default_Family, RFLX_Low_Order_First => Default_Family, RFLX_Case => Default_Family, RFLX_First => Default_Family, RFLX_Size => Default_Family, RFLX_Last => Default_Family, RFLX_Byte_Order => Default_Family, RFLX_Checksum => Default_Family, RFLX_Valid_Checksum => Default_Family, RFLX_Has_Data => Default_Family, RFLX_Head => Default_Family, RFLX_Opaque => Default_Family, RFLX_Present => Default_Family, RFLX_Valid => Default_Family, RFLX_Dot => Default_Family, RFLX_Comma => Default_Family, RFLX_Double_Dot => Default_Family, RFLX_Tick => Default_Family, RFLX_Hash => Default_Family, RFLX_Minus => Default_Family, RFLX_Arrow => Default_Family, RFLX_L_Par => Default_Family, RFLX_R_Par => Default_Family, RFLX_L_Brack => Default_Family, RFLX_R_Brack => Default_Family, RFLX_Exp => Default_Family, RFLX_Mul => Default_Family, RFLX_Div => Default_Family, RFLX_Add => Default_Family, RFLX_Sub => Default_Family, RFLX_Eq => Default_Family, RFLX_Neq => Default_Family, RFLX_Leq => Default_Family, RFLX_Lt => Default_Family, RFLX_Le => Default_Family, RFLX_Gt => Default_Family, RFLX_Ge => Default_Family, RFLX_And => Default_Family, RFLX_Or => Default_Family, RFLX_Ampersand => Default_Family, RFLX_Semicolon => Default_Family, RFLX_Double_Colon => Default_Family, RFLX_Assignment => Default_Family, RFLX_Colon => Default_Family, RFLX_Pipe => Default_Family, RFLX_Comment => Default_Family, RFLX_Numeral => Default_Family, RFLX_String_Literal => Default_Family);
   --  Associate a token family to all token kinds
   --
   --% document-value: False

   function Token_Kind_Name (Token_Id : Token_Kind) return String;
   --  Return a human-readable name for a token kind.

   function Token_Kind_Literal (Token_Id : Token_Kind) return Text_Type;
   --  Return the canonical literal corresponding to this token kind, or an
   --  empty string if this token has no literal.

   function Token_Error_Image (Token_Id : Token_Kind) return String;
   --  Return a string representation of ``Token_Id`` that is suitable in error
   --  messages.

   function To_Token_Kind (Raw : Raw_Token_Kind) return Token_Kind
      with Inline;
   function From_Token_Kind (Kind : Token_Kind) return Raw_Token_Kind
      with Inline;

   function Is_Token_Node (Kind : RFLX_Node_Kind_Type) return Boolean;
   --  Return whether Kind corresponds to a token node

   function Is_List_Node (Kind : RFLX_Node_Kind_Type) return Boolean;
   --  Return whether Kind corresponds to a list node

   function Is_Error_Node (Kind : RFLX_Node_Kind_Type) return Boolean;
   --  Return whether Kind corresponds to an error node

   type Visit_Status is (Into, Over, Stop);
   --  Helper type to control the node traversal process. See the
   --  ``Librflxlang.Analysis.Traverse`` function.

   -----------------------
   -- Lexical utilities --
   -----------------------

   type Token_Reference is private;
   --  Reference to a token in an analysis unit.

   No_Token : constant Token_Reference;

   type Token_Data_Type is private;

   function "<" (Left, Right : Token_Reference) return Boolean;
   --  Assuming ``Left`` and ``Right`` belong to the same analysis unit, return
   --  whether ``Left`` came before ``Right`` in the source file.

   function Next
     (Token          : Token_Reference;
      Exclude_Trivia : Boolean := False) return Token_Reference;
   --  Return a reference to the next token in the corresponding analysis unit.

   function Previous
     (Token          : Token_Reference;
      Exclude_Trivia : Boolean := False) return Token_Reference;
   --  Return a reference to the previous token in the corresponding analysis
   --  unit.

   function Data (Token : Token_Reference) return Token_Data_Type;
   --  Return the data associated to ``Token``

   function Is_Equivalent (L, R : Token_Reference) return Boolean;
   --  Return whether ``L`` and ``R`` are structurally equivalent tokens. This
   --  means that their position in the stream won't be taken into account,
   --  only the kind and text of the token.

   function Image (Token : Token_Reference) return String;
   --  Debug helper: return a human-readable text to represent a token

   function Text (Token : Token_Reference) return Text_Type;
   --  Return the text of the token as ``Text_Type``

   function Text (First, Last : Token_Reference) return Text_Type;
   --  Compute the source buffer slice corresponding to the text that spans
   --  between the ``First`` and ``Last`` tokens (both included). This yields
   --  an empty slice if ``Last`` actually appears before ``First``.
   --
   --  This raises a ``Constraint_Error`` if ``First`` and ``Last`` don't
   --  belong to the same analysis unit.

   function Get_Symbol (Token : Token_Reference) return Symbol_Type;
   --  Assuming that ``Token`` refers to a token that contains a symbol, return
   --  the corresponding symbol.

   function Kind (Token_Data : Token_Data_Type) return Token_Kind;
   --  Kind for this token.

   function Is_Trivia (Token : Token_Reference) return Boolean;
   --  Return whether this token is a trivia. If it's not, it's a regular
   --  token.

   function Is_Trivia (Token_Data : Token_Data_Type) return Boolean;
   --  Return whether this token is a trivia. If it's not, it's a regular
   --  token.

   function Index (Token : Token_Reference) return Token_Index;
   --  One-based index for this token/trivia. Tokens and trivias get their own
   --  index space.

   function Index (Token_Data : Token_Data_Type) return Token_Index;
   --  One-based index for this token/trivia. Tokens and trivias get their own
   --  index space.

   function Sloc_Range
     (Token_Data : Token_Data_Type) return Source_Location_Range;
   --  Source location range for this token. Note that the end bound is
   --  exclusive.

   function Origin_Filename (Token : Token_Reference) return String;
   --  Return the name of the file whose content was scanned to create Token.
   --  Return an empty string if the source comes from a memory buffer instead
   --  of a file.

   function Origin_Charset (Token : Token_Reference) return String;
   --  Return the charset used to decode the source that was scanned to create
   --  Token. Return an empty string if the source was already decoded during
   --  the scan.

   function Convert
     (TDH      : Token_Data_Handler;
      Token    : Token_Reference;
      Raw_Data : Stored_Token_Data) return Token_Data_Type;
   --  Turn data from ``TDH`` and ``Raw_Data`` into a user-ready token data
   --  record.

   type Child_Or_Trivia is (Child, Trivia);
   --  Discriminator for the ``Child_Record`` type

   function Raw_Data (T : Token_Reference) return Stored_Token_Data;
   --  Return the raw token data for ``T``

   Invalid_Input : exception renames Langkit_Support.Errors.Invalid_Input;
   --  Raised by lexing functions (``Librflxlang.Lexer``) when the input
   --  contains an invalid byte sequence.

   Invalid_Symbol_Error : exception renames Langkit_Support.Errors.Invalid_Symbol_Error;
   --  Exception raise when an invalid symbol is passed to a subprogram.

   Invalid_Unit_Name_Error : exception renames Langkit_Support.Errors.Invalid_Unit_Name_Error;
   --  Raised when an invalid unit name is provided.

   Native_Exception : exception renames Langkit_Support.Errors.Native_Exception;
   --  Exception raised in language bindings when the underlying C API reports
   --  an unexpected error that occurred in the library.
   --
   --  This kind of exception is raised for internal errors: they should never
   --  happen in normal situations and if they are raised at some point, it
   --  means the library state is potentially corrupted.
   --
   --  Nevertheless, the library does its best not to crash the program,
   --  materializing internal errors using this kind of exception.

   Precondition_Failure : exception renames Langkit_Support.Errors.Precondition_Failure;
   --  Exception raised when an API is called while its preconditions are not
   --  satisfied.

   Property_Error : exception renames Langkit_Support.Errors.Property_Error;
   --  Exception that is raised when an error occurs while evaluating any
   --  function whose name starts with ``P_``. This is the only exceptions that
   --  such functions can raise.

   Stale_Reference_Error : exception renames Langkit_Support.Errors.Stale_Reference_Error;
   --  Exception raised while trying to access data that was deallocated. This
   --  happens when one tries to use a node whose unit has been reparsed, for
   --  instance.

   Unknown_Charset : exception renames Langkit_Support.Errors.Unknown_Charset;
   --  Raised by lexing functions (``Librflxlang.Lexer``) when the input
   --  charset is not supported.

   -------------------
   -- Introspection --
   -------------------

   Bad_Type_Error : exception renames Langkit_Support.Errors.Introspection.Bad_Type_Error;
   --  Raised when introspection functions (``Librflxlang.Introspection``) are
   --  provided mismatching types/values.

   Out_Of_Bounds_Error : exception renames Langkit_Support.Errors.Introspection.Out_Of_Bounds_Error;
   --  Raised when introspection functions (``Librflxlang.Introspection``) are
   --  passed an out of bounds index.

   ---------------
   -- Rewriting --
   ---------------

   Template_Args_Error : exception renames Langkit_Support.Errors.Rewriting.Template_Args_Error;
   --  Exception raised when the provided arguments for a template don't match
   --  what the template expects.

   Template_Format_Error : exception renames Langkit_Support.Errors.Rewriting.Template_Format_Error;
   --  Exception raised when a template has an invalid syntax, such as badly
   --  formatted placeholders.

   Template_Instantiation_Error : exception renames Langkit_Support.Errors.Rewriting.Template_Instantiation_Error;
   --  Exception raised when the instantiation of a template cannot be parsed.


   -------------------
   -- Introspection --
   -------------------

   --  Unlike ``RFLX_Node_Kind_Type``, the following enumeration contains entries
   --  for abstract nodes.

   type Any_Node_Type_Id is (
      None, RFLX_Node_Type_Id, AbstractID_Type_Id, ID_Type_Id, UnqualifiedID_Type_Id, Aspect_Type_Id, Attr_Type_Id, Attr_First_Type_Id, Attr_Has_Data_Type_Id, Attr_Head_Type_Id, Attr_Last_Type_Id, Attr_Opaque_Type_Id, Attr_Present_Type_Id, Attr_Size_Type_Id, Attr_Valid_Type_Id, Attr_Valid_Checksum_Type_Id, Attr_Stmt_Type_Id, Attr_Stmt_Append_Type_Id, Attr_Stmt_Extend_Type_Id, Attr_Stmt_Read_Type_Id, Attr_Stmt_Write_Type_Id, Base_Aggregate_Type_Id, Message_Aggregate_Associations_Type_Id, Null_Message_Aggregate_Type_Id, Base_Checksum_Val_Type_Id, Checksum_Val_Type_Id, Checksum_Value_Range_Type_Id, Byte_Order_Type_Type_Id, Byte_Order_Type_Highorderfirst_Type_Id, Byte_Order_Type_Loworderfirst_Type_Id, Channel_Attribute_Type_Id, Readable_Type_Id, Writable_Type_Id, Checksum_Assoc_Type_Id, Declaration_Type_Id, Refinement_Decl_Type_Id, Session_Decl_Type_Id, Type_Decl_Type_Id, Description_Type_Id, Element_Value_Assoc_Type_Id, Expr_Type_Id, Attribute_Type_Id, Bin_Op_Type_Id, Binding_Type_Id, Call_Type_Id, Case_Expression_Type_Id, Choice_Type_Id, Comprehension_Type_Id, Context_Item_Type_Id, Conversion_Type_Id, Message_Aggregate_Type_Id, Negation_Type_Id, Numeric_Literal_Type_Id, Paren_Expression_Type_Id, Quantified_Expression_Type_Id, Select_Node_Type_Id, Sequence_Literal_Type_Id, Concatenation_Type_Id, Sequence_Aggregate_Type_Id, String_Literal_Type_Id, Variable_Type_Id, Formal_Decl_Type_Id, Formal_Channel_Decl_Type_Id, Formal_Function_Decl_Type_Id, Local_Decl_Type_Id, Renaming_Decl_Type_Id, Variable_Decl_Type_Id, Message_Aggregate_Association_Type_Id, Message_Aspect_Type_Id, Byte_Order_Aspect_Type_Id, Checksum_Aspect_Type_Id, Message_Field_Type_Id, Message_Fields_Type_Id, Null_Message_Field_Type_Id, Op_Type_Id, Op_Add_Type_Id, Op_And_Type_Id, Op_Div_Type_Id, Op_Eq_Type_Id, Op_Ge_Type_Id, Op_Gt_Type_Id, Op_In_Type_Id, Op_Le_Type_Id, Op_Lt_Type_Id, Op_Mod_Type_Id, Op_Mul_Type_Id, Op_Neq_Type_Id, Op_Notin_Type_Id, Op_Or_Type_Id, Op_Pow_Type_Id, Op_Sub_Type_Id, Package_Node_Type_Id, Parameter_Type_Id, Parameters_Type_Id, Quantifier_Type_Id, Quantifier_All_Type_Id, Quantifier_Some_Type_Id, RFLX_Node_Base_List_Type_Id, Aspect_List_Type_Id, Base_Checksum_Val_List_Type_Id, Channel_Attribute_List_Type_Id, Checksum_Assoc_List_Type_Id, Choice_List_Type_Id, Conditional_Transition_List_Type_Id, Context_Item_List_Type_Id, Declaration_List_Type_Id, Element_Value_Assoc_List_Type_Id, Expr_List_Type_Id, Formal_Decl_List_Type_Id, Local_Decl_List_Type_Id, Message_Aggregate_Association_List_Type_Id, Message_Aspect_List_Type_Id, Message_Field_List_Type_Id, Numeric_Literal_List_Type_Id, Parameter_List_Type_Id, RFLX_Node_List_Type_Id, State_List_Type_Id, Statement_List_Type_Id, Term_Assoc_List_Type_Id, Then_Node_List_Type_Id, Type_Argument_List_Type_Id, UnqualifiedID_List_Type_Id, Specification_Type_Id, State_Type_Id, State_Body_Type_Id, Statement_Type_Id, Assignment_Type_Id, Attribute_Statement_Type_Id, Message_Field_Assignment_Type_Id, Reset_Type_Id, Term_Assoc_Type_Id, Then_Node_Type_Id, Transition_Type_Id, Conditional_Transition_Type_Id, Type_Argument_Type_Id, Type_Def_Type_Id, Abstract_Message_Type_Def_Type_Id, Message_Type_Def_Type_Id, Null_Message_Type_Def_Type_Id, Enumeration_Def_Type_Id, Named_Enumeration_Def_Type_Id, Positional_Enumeration_Def_Type_Id, Enumeration_Type_Def_Type_Id, Integer_Type_Def_Type_Id, Modular_Type_Def_Type_Id, Range_Type_Def_Type_Id, Sequence_Type_Def_Type_Id, Type_Derivation_Def_Type_Id
   );

   subtype Node_Type_Id is Any_Node_Type_Id
      range RFLX_Node_Type_Id
            .. Type_Derivation_Def_Type_Id;

   type Node_Type_Id_Array is array (Positive range <>) of Node_Type_Id;

   type Any_Value_Kind is (
      None,
      Boolean_Value,
      Integer_Value,
      Big_Integer_Value,
      Character_Value,
      Token_Value,
      Unbounded_Text_Value,
      Analysis_Unit_Value,
      Node_Value

      , Analysis_Unit_Kind_Value
      , Lookup_Kind_Value
      , Grammar_Rule_Value

      , Text_Type_Value
      , RFLX_Node_Array_Value
   );
   subtype Value_Kind is
      Any_Value_Kind range Boolean_Value ..  Any_Value_Kind'Last;
   --  Enumeration for all types used to interact with properties

   
   subtype Enum_Value_Kind is Value_Kind with Static_Predicate =>
      Enum_Value_Kind in Analysis_Unit_Kind_Value | Lookup_Kind_Value | Grammar_Rule_Value;
   --  Subrange for all enum types

   
   subtype Array_Value_Kind is Value_Kind with Static_Predicate =>
      Array_Value_Kind in Text_Type_Value | RFLX_Node_Array_Value;
   --  Subrange for all array types

   subtype Struct_Value_Kind is Value_Kind
         range Any_Value_Kind'Last .. Any_Value_Kind'First
   ;
   --  Subrange for all struct types

   type Type_Constraint (Kind : Value_Kind := Value_Kind'First) is record
      case Kind is
         when Node_Value =>
            Node_Type : Node_Type_Id;
            --  Base type for nodes that satisfy this constraint

         when others =>
            null;
      end case;
   end record;
   --  Type constraint for a polymorphic value

   type Type_Constraint_Array is array (Positive range <>) of Type_Constraint;

   

   type Any_Member_Reference is
      (None, ID_F_Package, ID_F_Name, Aspect_F_Identifier, Aspect_F_Value, Message_Aggregate_Associations_F_Associations, Checksum_Val_F_Data, Checksum_Value_Range_F_First, Checksum_Value_Range_F_Last, Checksum_Assoc_F_Identifier, Checksum_Assoc_F_Covered_Fields, Refinement_Decl_F_Pdu, Refinement_Decl_F_Field, Refinement_Decl_F_Sdu, Refinement_Decl_F_Condition, Session_Decl_F_Parameters, Session_Decl_F_Identifier, Session_Decl_F_Declarations, Session_Decl_F_States, Session_Decl_F_End_Identifier, Type_Decl_F_Identifier, Type_Decl_F_Parameters, Type_Decl_F_Definition, Description_F_Content, Element_Value_Assoc_F_Identifier, Element_Value_Assoc_F_Literal, Attribute_F_Expression, Attribute_F_Kind, Bin_Op_F_Left, Bin_Op_F_Op, Bin_Op_F_Right, Binding_F_Expression, Binding_F_Bindings, Call_F_Identifier, Call_F_Arguments, Case_Expression_F_Expression, Case_Expression_F_Choices, Choice_F_Selectors, Choice_F_Expression, Comprehension_F_Iterator, Comprehension_F_Sequence, Comprehension_F_Condition, Comprehension_F_Selector, Context_Item_F_Item, Conversion_F_Target_Identifier, Conversion_F_Argument, Message_Aggregate_F_Identifier, Message_Aggregate_F_Values, Negation_F_Data, Paren_Expression_F_Data, Quantified_Expression_F_Operation, Quantified_Expression_F_Parameter_Identifier, Quantified_Expression_F_Iterable, Quantified_Expression_F_Predicate, Select_Node_F_Expression, Select_Node_F_Selector, Concatenation_F_Left, Concatenation_F_Right, Sequence_Aggregate_F_Values, Variable_F_Identifier, Formal_Channel_Decl_F_Identifier, Formal_Channel_Decl_F_Parameters, Formal_Function_Decl_F_Identifier, Formal_Function_Decl_F_Parameters, Formal_Function_Decl_F_Return_Type_Identifier, Renaming_Decl_F_Identifier, Renaming_Decl_F_Type_Identifier, Renaming_Decl_F_Expression, Variable_Decl_F_Identifier, Variable_Decl_F_Type_Identifier, Variable_Decl_F_Initializer, Message_Aggregate_Association_F_Identifier, Message_Aggregate_Association_F_Expression, Byte_Order_Aspect_F_Byte_Order, Checksum_Aspect_F_Associations, Message_Field_F_Identifier, Message_Field_F_Type_Identifier, Message_Field_F_Type_Arguments, Message_Field_F_Aspects, Message_Field_F_Condition, Message_Field_F_Thens, Message_Fields_F_Initial_Field, Message_Fields_F_Fields, Null_Message_Field_F_Then, Package_Node_F_Identifier, Package_Node_F_Declarations, Package_Node_F_End_Identifier, Parameter_F_Identifier, Parameter_F_Type_Identifier, Parameters_F_Parameters, Specification_F_Context_Clause, Specification_F_Package_Declaration, State_F_Identifier, State_F_Description, State_F_Body, State_Body_F_Declarations, State_Body_F_Actions, State_Body_F_Conditional_Transitions, State_Body_F_Final_Transition, State_Body_F_Exception_Transition, State_Body_F_End_Identifier, Assignment_F_Identifier, Assignment_F_Expression, Attribute_Statement_F_Identifier, Attribute_Statement_F_Attr, Attribute_Statement_F_Expression, Message_Field_Assignment_F_Message, Message_Field_Assignment_F_Field, Message_Field_Assignment_F_Expression, Reset_F_Identifier, Reset_F_Associations, Term_Assoc_F_Identifier, Term_Assoc_F_Expression, Then_Node_F_Target, Then_Node_F_Aspects, Then_Node_F_Condition, Transition_F_Target, Transition_F_Description, Conditional_Transition_F_Condition, Type_Argument_F_Identifier, Type_Argument_F_Expression, Message_Type_Def_F_Message_Fields, Message_Type_Def_F_Aspects, Named_Enumeration_Def_F_Elements, Positional_Enumeration_Def_F_Elements, Enumeration_Type_Def_F_Elements, Enumeration_Type_Def_F_Aspects, Modular_Type_Def_F_Mod, Range_Type_Def_F_First, Range_Type_Def_F_Last, Range_Type_Def_F_Size, Sequence_Type_Def_F_Element_Type, Type_Derivation_Def_F_Base, RFLX_Node_Parent, RFLX_Node_Parents, RFLX_Node_Children, RFLX_Node_Token_Start, RFLX_Node_Token_End, RFLX_Node_Child_Index, RFLX_Node_Previous_Sibling, RFLX_Node_Next_Sibling, RFLX_Node_Unit, RFLX_Node_Is_Ghost, RFLX_Node_Full_Sloc_Image);
   subtype Member_Reference is Any_Member_Reference range
      ID_F_Package
      ..  RFLX_Node_Full_Sloc_Image;
   --  Enumeration of all data attached to structs/nodes (fields and
   --  properties).

   subtype Node_Member_Reference is Member_Reference range
      ID_F_Package
      ..  RFLX_Node_Full_Sloc_Image;
   --  Subrange for members of nodes only

   type Member_Reference_Array is
      array (Positive range <>) of Member_Reference;

   subtype Struct_Field_Reference is Member_Reference range
         
      RFLX_Node_Full_Sloc_Image
      .. ID_F_Package
   ;

   type Struct_Field_Reference_Array is
      array (Positive range <>) of Struct_Field_Reference;

   subtype Syntax_Field_Reference is Member_Reference range
         
      ID_F_Package
      .. Type_Derivation_Def_F_Base
   ;
   --  Enumeration of all syntax fields for regular nodes

   type Syntax_Field_Reference_Array is
      array (Positive range <>) of Syntax_Field_Reference;

   subtype Property_Reference is Member_Reference
      range RFLX_Node_Parent
         .. RFLX_Node_Full_Sloc_Image;
   --  Enumeration of all available node properties

   type Property_Reference_Array is
      array (Positive range <>) of Property_Reference;

   


private

   type Token_Reference is record
      TDH : Token_Data_Handler_Access;
      --  Token data handler that owns this token

      Index : Token_Or_Trivia_Index;
      --  Identifier for the trivia or the token this refers to
   end record;

   No_Token : constant Token_Reference := (null, No_Token_Or_Trivia_Index);

   type Token_Data_Type is record
      Kind : Token_Kind;
      --  See documentation for the Kind accessor

      Is_Trivia : Boolean;
      --  See documentation for the Is_Trivia accessor

      Index : Token_Index;
      --  See documentation for the Index accessor

      Source_Buffer : Text_Cst_Access;
      --  Text for the original source file

      Source_First : Positive;
      Source_Last  : Natural;
      --  Bounds in Source_Buffer for the text corresponding to this token

      Sloc_Range : Source_Location_Range;
      --  See documenation for the Sloc_Range accessor
   end record;

end Librflxlang.Common;
