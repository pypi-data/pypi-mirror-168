
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

with GNATCOLL.Iconv;
with GNATCOLL.VFS; use GNATCOLL.VFS;

with Librflxlang.Lexer_Implementation;
use Librflxlang.Lexer_Implementation;
with Librflxlang.Private_Converters;



package body Librflxlang.Common is

   Is_Token_Node_Kind : constant array (RFLX_Node_Kind_Type) of Boolean :=
     (RFLX_ID => False, RFLX_UnqualifiedID => True, RFLX_Aspect => False, RFLX_Attr_First => False, RFLX_Attr_Has_Data => False, RFLX_Attr_Head => False, RFLX_Attr_Last => False, RFLX_Attr_Opaque => False, RFLX_Attr_Present => False, RFLX_Attr_Size => False, RFLX_Attr_Valid => False, RFLX_Attr_Valid_Checksum => False, RFLX_Attr_Stmt_Append => False, RFLX_Attr_Stmt_Extend => False, RFLX_Attr_Stmt_Read => False, RFLX_Attr_Stmt_Write => False, RFLX_Message_Aggregate_Associations => False, RFLX_Null_Message_Aggregate => False, RFLX_Checksum_Val => False, RFLX_Checksum_Value_Range => False, RFLX_Byte_Order_Type_Highorderfirst => False, RFLX_Byte_Order_Type_Loworderfirst => False, RFLX_Readable => False, RFLX_Writable => False, RFLX_Checksum_Assoc => False, RFLX_Refinement_Decl => False, RFLX_Session_Decl => False, RFLX_Type_Decl => False, RFLX_Description => False, RFLX_Element_Value_Assoc => False, RFLX_Attribute => False, RFLX_Bin_Op => False, RFLX_Binding => False, RFLX_Call => False, RFLX_Case_Expression => False, RFLX_Choice => False, RFLX_Comprehension => False, RFLX_Context_Item => False, RFLX_Conversion => False, RFLX_Message_Aggregate => False, RFLX_Negation => False, RFLX_Numeric_Literal => True, RFLX_Paren_Expression => False, RFLX_Quantified_Expression => False, RFLX_Select_Node => False, RFLX_Concatenation => False, RFLX_Sequence_Aggregate => False, RFLX_String_Literal => True, RFLX_Variable => False, RFLX_Formal_Channel_Decl => False, RFLX_Formal_Function_Decl => False, RFLX_Renaming_Decl => False, RFLX_Variable_Decl => False, RFLX_Message_Aggregate_Association => False, RFLX_Byte_Order_Aspect => False, RFLX_Checksum_Aspect => False, RFLX_Message_Field => False, RFLX_Message_Fields => False, RFLX_Null_Message_Field => False, RFLX_Op_Add => False, RFLX_Op_And => False, RFLX_Op_Div => False, RFLX_Op_Eq => False, RFLX_Op_Ge => False, RFLX_Op_Gt => False, RFLX_Op_In => False, RFLX_Op_Le => False, RFLX_Op_Lt => False, RFLX_Op_Mod => False, RFLX_Op_Mul => False, RFLX_Op_Neq => False, RFLX_Op_Notin => False, RFLX_Op_Or => False, RFLX_Op_Pow => False, RFLX_Op_Sub => False, RFLX_Package_Node => False, RFLX_Parameter => False, RFLX_Parameters => False, RFLX_Quantifier_All => False, RFLX_Quantifier_Some => False, RFLX_Aspect_List => False, RFLX_Base_Checksum_Val_List => False, RFLX_Channel_Attribute_List => False, RFLX_Checksum_Assoc_List => False, RFLX_Choice_List => False, RFLX_Conditional_Transition_List => False, RFLX_Context_Item_List => False, RFLX_Declaration_List => False, RFLX_Element_Value_Assoc_List => False, RFLX_Expr_List => False, RFLX_Formal_Decl_List => False, RFLX_Local_Decl_List => False, RFLX_Message_Aggregate_Association_List => False, RFLX_Message_Aspect_List => False, RFLX_Message_Field_List => False, RFLX_Numeric_Literal_List => False, RFLX_Parameter_List => False, RFLX_RFLX_Node_List => False, RFLX_State_List => False, RFLX_Statement_List => False, RFLX_Term_Assoc_List => False, RFLX_Then_Node_List => False, RFLX_Type_Argument_List => False, RFLX_UnqualifiedID_List => False, RFLX_Specification => False, RFLX_State => False, RFLX_State_Body => False, RFLX_Assignment => False, RFLX_Attribute_Statement => False, RFLX_Message_Field_Assignment => False, RFLX_Reset => False, RFLX_Term_Assoc => False, RFLX_Then_Node => False, RFLX_Transition => False, RFLX_Conditional_Transition => False, RFLX_Type_Argument => False, RFLX_Message_Type_Def => False, RFLX_Null_Message_Type_Def => False, RFLX_Named_Enumeration_Def => False, RFLX_Positional_Enumeration_Def => False, RFLX_Enumeration_Type_Def => False, RFLX_Modular_Type_Def => False, RFLX_Range_Type_Def => False, RFLX_Sequence_Type_Def => False, RFLX_Type_Derivation_Def => False);
   --  For each node kind, return whether it is a node that contains only a
   --  single token.

   Is_Error_Node_Kind : constant array (RFLX_Node_Kind_Type) of Boolean :=
     (RFLX_ID => False, RFLX_UnqualifiedID => False, RFLX_Aspect => False, RFLX_Attr_First => False, RFLX_Attr_Has_Data => False, RFLX_Attr_Head => False, RFLX_Attr_Last => False, RFLX_Attr_Opaque => False, RFLX_Attr_Present => False, RFLX_Attr_Size => False, RFLX_Attr_Valid => False, RFLX_Attr_Valid_Checksum => False, RFLX_Attr_Stmt_Append => False, RFLX_Attr_Stmt_Extend => False, RFLX_Attr_Stmt_Read => False, RFLX_Attr_Stmt_Write => False, RFLX_Message_Aggregate_Associations => False, RFLX_Null_Message_Aggregate => False, RFLX_Checksum_Val => False, RFLX_Checksum_Value_Range => False, RFLX_Byte_Order_Type_Highorderfirst => False, RFLX_Byte_Order_Type_Loworderfirst => False, RFLX_Readable => False, RFLX_Writable => False, RFLX_Checksum_Assoc => False, RFLX_Refinement_Decl => False, RFLX_Session_Decl => False, RFLX_Type_Decl => False, RFLX_Description => False, RFLX_Element_Value_Assoc => False, RFLX_Attribute => False, RFLX_Bin_Op => False, RFLX_Binding => False, RFLX_Call => False, RFLX_Case_Expression => False, RFLX_Choice => False, RFLX_Comprehension => False, RFLX_Context_Item => False, RFLX_Conversion => False, RFLX_Message_Aggregate => False, RFLX_Negation => False, RFLX_Numeric_Literal => False, RFLX_Paren_Expression => False, RFLX_Quantified_Expression => False, RFLX_Select_Node => False, RFLX_Concatenation => False, RFLX_Sequence_Aggregate => False, RFLX_String_Literal => False, RFLX_Variable => False, RFLX_Formal_Channel_Decl => False, RFLX_Formal_Function_Decl => False, RFLX_Renaming_Decl => False, RFLX_Variable_Decl => False, RFLX_Message_Aggregate_Association => False, RFLX_Byte_Order_Aspect => False, RFLX_Checksum_Aspect => False, RFLX_Message_Field => False, RFLX_Message_Fields => False, RFLX_Null_Message_Field => False, RFLX_Op_Add => False, RFLX_Op_And => False, RFLX_Op_Div => False, RFLX_Op_Eq => False, RFLX_Op_Ge => False, RFLX_Op_Gt => False, RFLX_Op_In => False, RFLX_Op_Le => False, RFLX_Op_Lt => False, RFLX_Op_Mod => False, RFLX_Op_Mul => False, RFLX_Op_Neq => False, RFLX_Op_Notin => False, RFLX_Op_Or => False, RFLX_Op_Pow => False, RFLX_Op_Sub => False, RFLX_Package_Node => False, RFLX_Parameter => False, RFLX_Parameters => False, RFLX_Quantifier_All => False, RFLX_Quantifier_Some => False, RFLX_Aspect_List => False, RFLX_Base_Checksum_Val_List => False, RFLX_Channel_Attribute_List => False, RFLX_Checksum_Assoc_List => False, RFLX_Choice_List => False, RFLX_Conditional_Transition_List => False, RFLX_Context_Item_List => False, RFLX_Declaration_List => False, RFLX_Element_Value_Assoc_List => False, RFLX_Expr_List => False, RFLX_Formal_Decl_List => False, RFLX_Local_Decl_List => False, RFLX_Message_Aggregate_Association_List => False, RFLX_Message_Aspect_List => False, RFLX_Message_Field_List => False, RFLX_Numeric_Literal_List => False, RFLX_Parameter_List => False, RFLX_RFLX_Node_List => False, RFLX_State_List => False, RFLX_Statement_List => False, RFLX_Term_Assoc_List => False, RFLX_Then_Node_List => False, RFLX_Type_Argument_List => False, RFLX_UnqualifiedID_List => False, RFLX_Specification => False, RFLX_State => False, RFLX_State_Body => False, RFLX_Assignment => False, RFLX_Attribute_Statement => False, RFLX_Message_Field_Assignment => False, RFLX_Reset => False, RFLX_Term_Assoc => False, RFLX_Then_Node => False, RFLX_Transition => False, RFLX_Conditional_Transition => False, RFLX_Type_Argument => False, RFLX_Message_Type_Def => False, RFLX_Null_Message_Type_Def => False, RFLX_Named_Enumeration_Def => False, RFLX_Positional_Enumeration_Def => False, RFLX_Enumeration_Type_Def => False, RFLX_Modular_Type_Def => False, RFLX_Range_Type_Def => False, RFLX_Sequence_Type_Def => False, RFLX_Type_Derivation_Def => False);
   --  For each node kind, return whether it is an error node

   function Wrap_Token_Reference
     (TDH   : Token_Data_Handler_Access;
      Index : Token_Or_Trivia_Index) return Token_Reference;
   function Get_Token_TDH
     (Token : Token_Reference) return Token_Data_Handler_Access;
   function Get_Token_Index
     (Token : Token_Reference) return Token_Or_Trivia_Index;
   procedure Extract_Token_Text
     (Token         : Token_Data_Type;
      Source_Buffer : out Text_Cst_Access;
      First         : out Positive;
      Last          : out Natural);
   --  Implementations for converters soft-links

   Token_Kind_To_Literals : constant array (Token_Kind) of Text_Access := (
   

         RFLX_Unqualified_Identifier => new Text_Type'("First"),
         
         RFLX_Valid_Checksum => new Text_Type'("Valid_Checksum"),
         
         RFLX_Has_Data => new Text_Type'("Has_Data"),
         
         RFLX_Head => new Text_Type'("Head"),
         
         RFLX_Opaque => new Text_Type'("Opaque"),
         
         RFLX_Present => new Text_Type'("Present"),
         
         RFLX_Valid => new Text_Type'("Valid"),
         
         RFLX_Checksum => new Text_Type'("Checksum"),
         
         RFLX_Package => new Text_Type'("package"),
         
         RFLX_Is => new Text_Type'("is"),
         
         RFLX_If => new Text_Type'("if"),
         
         RFLX_End => new Text_Type'("end"),
         
         RFLX_Null => new Text_Type'("null"),
         
         RFLX_Type => new Text_Type'("type"),
         
         RFLX_Range => new Text_Type'("range"),
         
         RFLX_With => new Text_Type'("with"),
         
         RFLX_Mod => new Text_Type'("mod"),
         
         RFLX_Message => new Text_Type'("message"),
         
         RFLX_Then => new Text_Type'("then"),
         
         RFLX_Sequence => new Text_Type'("sequence"),
         
         RFLX_Of => new Text_Type'("of"),
         
         RFLX_In => new Text_Type'("in"),
         
         RFLX_Not => new Text_Type'("not"),
         
         RFLX_New => new Text_Type'("new"),
         
         RFLX_For => new Text_Type'("for"),
         
         RFLX_When => new Text_Type'("when"),
         
         RFLX_Where => new Text_Type'("where"),
         
         RFLX_Use => new Text_Type'("use"),
         
         RFLX_All => new Text_Type'("all"),
         
         RFLX_Some => new Text_Type'("some"),
         
         RFLX_Generic => new Text_Type'("generic"),
         
         RFLX_Session => new Text_Type'("session"),
         
         RFLX_Begin => new Text_Type'("begin"),
         
         RFLX_Return => new Text_Type'("return"),
         
         RFLX_Function => new Text_Type'("function"),
         
         RFLX_State => new Text_Type'("state"),
         
         RFLX_Transition => new Text_Type'("transition"),
         
         RFLX_Goto => new Text_Type'("goto"),
         
         RFLX_Exception => new Text_Type'("exception"),
         
         RFLX_Renames => new Text_Type'("renames"),
         
         RFLX_Case => new Text_Type'("case"),
         
         RFLX_Channel => new Text_Type'("Channel"),
         
         RFLX_Readable => new Text_Type'("Readable"),
         
         RFLX_Writable => new Text_Type'("Writable"),
         
         RFLX_Desc => new Text_Type'("Desc"),
         
         RFLX_Append => new Text_Type'("Append"),
         
         RFLX_Extend => new Text_Type'("Extend"),
         
         RFLX_Read => new Text_Type'("Read"),
         
         RFLX_Write => new Text_Type'("Write"),
         
         RFLX_Reset => new Text_Type'("Reset"),
         
         RFLX_Byte_Order => new Text_Type'("Byte_Order"),
         
         RFLX_High_Order_First => new Text_Type'("High_Order_First"),
         
         RFLX_Low_Order_First => new Text_Type'("Low_Order_First"),
         
         RFLX_Semicolon => new Text_Type'(";"),
         
         RFLX_Double_Colon => new Text_Type'("::"),
         
         RFLX_Assignment => new Text_Type'(":="),
         
         RFLX_Colon => new Text_Type'(":"),
         
         RFLX_L_Par => new Text_Type'("("),
         
         RFLX_R_Par => new Text_Type'(")"),
         
         RFLX_L_Brack => new Text_Type'("["),
         
         RFLX_R_Brack => new Text_Type'("]"),
         
         RFLX_Double_Dot => new Text_Type'(".."),
         
         RFLX_Dot => new Text_Type'("."),
         
         RFLX_Comma => new Text_Type'(","),
         
         RFLX_Tick => new Text_Type'("'"),
         
         RFLX_Hash => new Text_Type'("#"),
         
         RFLX_Exp => new Text_Type'("**"),
         
         RFLX_Mul => new Text_Type'("*"),
         
         RFLX_Neq => new Text_Type'("/="),
         
         RFLX_Div => new Text_Type'("/"),
         
         RFLX_Add => new Text_Type'("+"),
         
         RFLX_Sub => new Text_Type'("-"),
         
         RFLX_Eq => new Text_Type'("="),
         
         RFLX_Le => new Text_Type'("<="),
         
         RFLX_Lt => new Text_Type'("<"),
         
         RFLX_Ge => new Text_Type'(">="),
         
         RFLX_Gt => new Text_Type'(">"),
         
         RFLX_Pipe => new Text_Type'("|"),
         
         RFLX_And => new Text_Type'("and"),
         
         RFLX_Or => new Text_Type'("or"),
         
         RFLX_Ampersand => new Text_Type'("&"),
         
         RFLX_Arrow => new Text_Type'("=>"),
         
      others => new Text_Type'("")
   );

   Token_Kind_Names : constant array (Token_Kind) of String_Access := (
          RFLX_Unqualified_Identifier =>
             new String'("Unqualified_Identifier")
              ,
          RFLX_Package =>
             new String'("Package")
              ,
          RFLX_Is =>
             new String'("Is")
              ,
          RFLX_If =>
             new String'("If")
              ,
          RFLX_End =>
             new String'("End")
              ,
          RFLX_Null =>
             new String'("Null")
              ,
          RFLX_Type =>
             new String'("Type")
              ,
          RFLX_Range =>
             new String'("Range")
              ,
          RFLX_With =>
             new String'("With")
              ,
          RFLX_Mod =>
             new String'("Mod")
              ,
          RFLX_Message =>
             new String'("Message")
              ,
          RFLX_Then =>
             new String'("Then")
              ,
          RFLX_Sequence =>
             new String'("Sequence")
              ,
          RFLX_Of =>
             new String'("Of")
              ,
          RFLX_In =>
             new String'("In")
              ,
          RFLX_Not =>
             new String'("Not")
              ,
          RFLX_New =>
             new String'("New")
              ,
          RFLX_For =>
             new String'("For")
              ,
          RFLX_When =>
             new String'("When")
              ,
          RFLX_Where =>
             new String'("Where")
              ,
          RFLX_Use =>
             new String'("Use")
              ,
          RFLX_All =>
             new String'("All")
              ,
          RFLX_Some =>
             new String'("Some")
              ,
          RFLX_Generic =>
             new String'("Generic")
              ,
          RFLX_Session =>
             new String'("Session")
              ,
          RFLX_Begin =>
             new String'("Begin")
              ,
          RFLX_Return =>
             new String'("Return")
              ,
          RFLX_Function =>
             new String'("Function")
              ,
          RFLX_State =>
             new String'("State")
              ,
          RFLX_Transition =>
             new String'("Transition")
              ,
          RFLX_Goto =>
             new String'("Goto")
              ,
          RFLX_Exception =>
             new String'("Exception")
              ,
          RFLX_Renames =>
             new String'("Renames")
              ,
          RFLX_Channel =>
             new String'("Channel")
              ,
          RFLX_Readable =>
             new String'("Readable")
              ,
          RFLX_Writable =>
             new String'("Writable")
              ,
          RFLX_Desc =>
             new String'("Desc")
              ,
          RFLX_Append =>
             new String'("Append")
              ,
          RFLX_Extend =>
             new String'("Extend")
              ,
          RFLX_Read =>
             new String'("Read")
              ,
          RFLX_Write =>
             new String'("Write")
              ,
          RFLX_Reset =>
             new String'("Reset")
              ,
          RFLX_High_Order_First =>
             new String'("High_Order_First")
              ,
          RFLX_Low_Order_First =>
             new String'("Low_Order_First")
              ,
          RFLX_Case =>
             new String'("Case")
              ,
          RFLX_First =>
             new String'("First")
              ,
          RFLX_Size =>
             new String'("Size")
              ,
          RFLX_Last =>
             new String'("Last")
              ,
          RFLX_Byte_Order =>
             new String'("Byte_Order")
              ,
          RFLX_Checksum =>
             new String'("Checksum")
              ,
          RFLX_Valid_Checksum =>
             new String'("Valid_Checksum")
              ,
          RFLX_Has_Data =>
             new String'("Has_Data")
              ,
          RFLX_Head =>
             new String'("Head")
              ,
          RFLX_Opaque =>
             new String'("Opaque")
              ,
          RFLX_Present =>
             new String'("Present")
              ,
          RFLX_Valid =>
             new String'("Valid")
              ,
          RFLX_Dot =>
             new String'("Dot")
              ,
          RFLX_Comma =>
             new String'("Comma")
              ,
          RFLX_Double_Dot =>
             new String'("Double_Dot")
              ,
          RFLX_Tick =>
             new String'("Tick")
              ,
          RFLX_Hash =>
             new String'("Hash")
              ,
          RFLX_Minus =>
             new String'("Minus")
              ,
          RFLX_Arrow =>
             new String'("Arrow")
              ,
          RFLX_L_Par =>
             new String'("L_Par")
              ,
          RFLX_R_Par =>
             new String'("R_Par")
              ,
          RFLX_L_Brack =>
             new String'("L_Brack")
              ,
          RFLX_R_Brack =>
             new String'("R_Brack")
              ,
          RFLX_Exp =>
             new String'("Exp")
              ,
          RFLX_Mul =>
             new String'("Mul")
              ,
          RFLX_Div =>
             new String'("Div")
              ,
          RFLX_Add =>
             new String'("Add")
              ,
          RFLX_Sub =>
             new String'("Sub")
              ,
          RFLX_Eq =>
             new String'("Eq")
              ,
          RFLX_Neq =>
             new String'("Neq")
              ,
          RFLX_Leq =>
             new String'("Leq")
              ,
          RFLX_Lt =>
             new String'("Lt")
              ,
          RFLX_Le =>
             new String'("Le")
              ,
          RFLX_Gt =>
             new String'("Gt")
              ,
          RFLX_Ge =>
             new String'("Ge")
              ,
          RFLX_And =>
             new String'("And")
              ,
          RFLX_Or =>
             new String'("Or")
              ,
          RFLX_Ampersand =>
             new String'("Ampersand")
              ,
          RFLX_Semicolon =>
             new String'("Semicolon")
              ,
          RFLX_Double_Colon =>
             new String'("Double_Colon")
              ,
          RFLX_Assignment =>
             new String'("Assignment")
              ,
          RFLX_Colon =>
             new String'("Colon")
              ,
          RFLX_Pipe =>
             new String'("Pipe")
              ,
          RFLX_Comment =>
             new String'("Comment")
              ,
          RFLX_Numeral =>
             new String'("Numeral")
              ,
          RFLX_String_Literal =>
             new String'("String_Literal")
              ,
          RFLX_Termination =>
             new String'("Termination")
              ,
          RFLX_Lexing_Failure =>
             new String'("Lexing_Failure")
   );

   ------------------------
   -- Precomputed_Symbol --
   ------------------------

   pragma Warnings (Off, "referenced");
   function Precomputed_Symbol
     (Index : Precomputed_Symbol_Index) return Text_Type is
   pragma Warnings (On, "referenced");
   begin
         return (raise Program_Error);
   end Precomputed_Symbol;

   ---------------------
   -- Token_Kind_Name --
   ---------------------

   function Token_Kind_Name (Token_Id : Token_Kind) return String is
     (Token_Kind_Names (Token_Id).all);

   ------------------------
   -- Token_Kind_Literal --
   ------------------------

   function Token_Kind_Literal (Token_Id : Token_Kind) return Text_Type is
     (Token_Kind_To_Literals (Token_Id).all);

   -----------------------
   -- Token_Error_Image --
   -----------------------

   function Token_Error_Image (Token_Id : Token_Kind) return String is
      Literal : constant Text_Type := Token_Kind_Literal (Token_Id);
   begin
      return (if Literal /= ""
              then "'" & Image (Literal) & "'"
              else Token_Kind_Name (Token_Id));
   end Token_Error_Image;

   function To_Token_Kind (Raw : Raw_Token_Kind) return Token_Kind
   is (Token_Kind'Val (Raw));

   function From_Token_Kind (Kind : Token_Kind) return Raw_Token_Kind
   is (Token_Kind'Pos (Kind));

   -------------------
   -- Is_Token_Node --
   -------------------

   function Is_Token_Node (Kind : RFLX_Node_Kind_Type) return Boolean is
   begin
      return Is_Token_Node_Kind (Kind);
   end Is_Token_Node;

   -------------------
   -- Is_Error_Node --
   -------------------

   function Is_Error_Node (Kind : RFLX_Node_Kind_Type) return Boolean is
   begin
      return Is_Error_Node_Kind (Kind);
   end Is_Error_Node;

   ------------------
   -- Is_List_Node --
   ------------------

   function Is_List_Node (Kind : RFLX_Node_Kind_Type) return Boolean is
   begin
      return Kind in RFLX_RFLX_Node_Base_List;
   end Is_List_Node;

   ---------
   -- "<" --
   ---------

   function "<" (Left, Right : Token_Reference) return Boolean is
      pragma Assert (Left.TDH = Right.TDH);
   begin
      if Left.Index.Token < Right.Index.Token then
         return True;

      elsif Left.Index.Token = Right.Index.Token then
         return Left.Index.Trivia < Right.Index.Trivia;

      else
         return False;
      end if;
   end "<";

   ----------
   -- Next --
   ----------

   function Next
     (Token          : Token_Reference;
      Exclude_Trivia : Boolean := False) return Token_Reference is
   begin
      return (if Token.TDH = null
              then No_Token
              else Wrap_Token_Reference (Token.TDH,
                                         Next (Token.Index, Token.TDH.all,
                                               Exclude_Trivia)));
   end Next;

   --------------
   -- Previous --
   --------------

   function Previous
     (Token          : Token_Reference;
      Exclude_Trivia : Boolean := False) return Token_Reference is
   begin
      return
        (if Token.TDH = null
         then No_Token
         else Wrap_Token_Reference (Token.TDH,
                                    Previous (Token.Index, Token.TDH.all,
                                              Exclude_Trivia)));
   end Previous;

   ----------------
   -- Get_Symbol --
   ----------------

   function Get_Symbol (Token : Token_Reference) return Symbol_Type is
   begin
      if Token.TDH = null then
         raise Precondition_Failure with "null token argument";
      end if;
      return Get_Symbol (Token.Index, Token.TDH.all);
   end Get_Symbol;

   ----------
   -- Data --
   ----------

   function Data (Token : Token_Reference) return Token_Data_Type is
   begin
      if Token.TDH = null then
         raise Precondition_Failure with "null token argument";
      end if;
      return Convert (Token.TDH.all, Token, Raw_Data (Token));
   end Data;

   ----------
   -- Text --
   ----------

   function Text (Token : Token_Reference) return Text_Type is
      RD : constant Stored_Token_Data := Raw_Data (Token);
   begin
      if Token.TDH = null then
         raise Precondition_Failure with "null token argument";
      end if;
      return Token.TDH.Source_Buffer (RD.Source_First .. RD.Source_Last);
   end Text;

   ----------
   -- Text --
   ----------

   function Text (First, Last : Token_Reference) return Text_Type is
      FD : constant Token_Data_Type := Data (First);
      LD : constant Token_Data_Type := Data (Last);
   begin
      if First.TDH = null then
         raise Precondition_Failure with "null token argument";
      end if;
      if First.TDH /= Last.TDH then
         raise Precondition_Failure with
            "token arguments must belong to the same source";
      end if;
      return FD.Source_Buffer.all (FD.Source_First .. LD.Source_Last);
   end Text;

   ----------
   -- Kind --
   ----------

   function Kind (Token_Data : Token_Data_Type) return Token_Kind is
   begin
      return Token_Data.Kind;
   end Kind;

   ---------------
   -- Is_Trivia --
   ---------------

   function Is_Trivia (Token : Token_Reference) return Boolean is
   begin
      return Token.Index.Trivia /= No_Token_Index;
   end Is_Trivia;

   ---------------
   -- Is_Trivia --
   ---------------

   function Is_Trivia (Token_Data : Token_Data_Type) return Boolean is
   begin
      return Token_Data.Is_Trivia;
   end Is_Trivia;

   -----------
   -- Index --
   -----------

   function Index (Token : Token_Reference) return Token_Index is
   begin
      return (if Token.Index.Trivia = No_Token_Index
              then Token.Index.Token
              else Token.Index.Trivia);
   end Index;

   -----------
   -- Index --
   -----------

   function Index (Token_Data : Token_Data_Type) return Token_Index is
   begin
      return Token_Data.Index;
   end Index;

   ----------------
   -- Sloc_Range --
   ----------------

   function Sloc_Range
     (Token_Data : Token_Data_Type) return Source_Location_Range
   is
   begin
      return Token_Data.Sloc_Range;
   end Sloc_Range;

   ---------------------
   -- Origin_Filename --
   ---------------------

   function Origin_Filename (Token : Token_Reference) return String is
   begin
      if Token.TDH = null then
         raise Precondition_Failure with "null token argument";
      end if;
      return +Token.TDH.Filename.Full_Name;
   end Origin_Filename;

   --------------------
   -- Origin_Charset --
   --------------------

   function Origin_Charset (Token : Token_Reference) return String is
   begin
      if Token.TDH = null then
         raise Precondition_Failure with "null token argument";
      end if;
      return To_String (Token.TDH.Charset);
   end Origin_Charset;

   -------------------
   -- Is_Equivalent --
   -------------------

   function Is_Equivalent (L, R : Token_Reference) return Boolean is
      DL : constant Token_Data_Type := Data (L);
      DR : constant Token_Data_Type := Data (R);
      TL : constant Text_Type := Text (L);
      TR : constant Text_Type := Text (R);
   begin
      return DL.Kind = DR.Kind and then TL = TR;
   end Is_Equivalent;

   -----------
   -- Image --
   -----------

   function Image (Token : Token_Reference) return String is
      D : constant Token_Data_Type := Data (Token);
   begin
      return ("<Token Kind=" & Token_Kind_Name (D.Kind) &
              " Text=" & Image (Text (Token), With_Quotes => True) & ">");
   end Image;

   --------------
   -- Raw_Data --
   --------------

   function Raw_Data (T : Token_Reference) return Stored_Token_Data is
   begin
      if T.TDH = null then
         raise Precondition_Failure with "null token argument";
      end if;
      return
        (if T.Index.Trivia = No_Token_Index
         then Token_Vectors.Get (T.TDH.Tokens, Natural (T.Index.Token))
         else Trivia_Vectors.Get (T.TDH.Trivias, Natural (T.Index.Trivia)).T);
   end Raw_Data;

   -------------
   -- Convert --
   -------------

   function Convert
     (TDH      : Token_Data_Handler;
      Token    : Token_Reference;
      Raw_Data : Stored_Token_Data) return Token_Data_Type is
   begin
      return (Kind          => To_Token_Kind (Raw_Data.Kind),
              Is_Trivia     => Token.Index.Trivia /= No_Token_Index,
              Index         => (if Token.Index.Trivia = No_Token_Index
                                then Token.Index.Token
                                else Token.Index.Trivia),
              Source_Buffer => Text_Cst_Access (TDH.Source_Buffer),
              Source_First  => Raw_Data.Source_First,
              Source_Last   => Raw_Data.Source_Last,
              Sloc_Range    => Sloc_Range (TDH, Raw_Data));
   end Convert;

   --------------------------
   -- Wrap_Token_Reference --
   --------------------------

   function Wrap_Token_Reference
     (TDH   : Token_Data_Handler_Access;
      Index : Token_Or_Trivia_Index) return Token_Reference is
   begin
      return (if Index = No_Token_Or_Trivia_Index
              then No_Token
              else (TDH, Index));
   end Wrap_Token_Reference;

   -------------------
   -- Get_Token_TDH --
   -------------------

   function Get_Token_TDH
     (Token : Token_Reference) return Token_Data_Handler_Access is
   begin
      return Token.TDH;
   end Get_Token_TDH;

   ---------------------
   -- Get_Token_Index --
   ---------------------

   function Get_Token_Index
     (Token : Token_Reference) return Token_Or_Trivia_Index is
   begin
      return Token.Index;
   end Get_Token_Index;

   ------------------------
   -- Extract_Token_Text --
   ------------------------

   procedure Extract_Token_Text
     (Token         : Token_Data_Type;
      Source_Buffer : out Text_Cst_Access;
      First         : out Positive;
      Last          : out Natural) is
   begin
      Source_Buffer := Token.Source_Buffer;
      First := Token.Source_First;
      Last := Token.Source_Last;
   end Extract_Token_Text;


begin
   --  Check that we actually have full Libiconv support: as nothing works
   --  without it, we explicitly check support here instead of letting
   --  user-unfriendly errors happen during lexing.

   if not GNATCOLL.Iconv.Has_Iconv then
      raise Program_Error with "Libiconv is not available";
   end if;


   Private_Converters.Wrap_Token_Reference := Wrap_Token_Reference'Access;
   Private_Converters.Get_Token_TDH := Get_Token_TDH'Access;
   Private_Converters.Get_Token_Index := Get_Token_Index'Access;
   Private_Converters.Extract_Token_Text := Extract_Token_Text'Access;
end Librflxlang.Common;
