
with Langkit_Support.Text; use Langkit_Support.Text;
with Langkit_Support.Token_Data_Handlers;
use Langkit_Support.Token_Data_Handlers;

with Librflxlang.Common;         use Librflxlang.Common;
with Librflxlang.Implementation; use Librflxlang.Implementation;

--  Internal package: provide implementation helpers to switch between public
--  types and implementation ones.

private package Librflxlang.Private_Converters is

   type Token_Reference_Wrapper is access function
     (TDH   : Token_Data_Handler_Access;
      Index : Token_Or_Trivia_Index) return Token_Reference;
   Wrap_Token_Reference : Token_Reference_Wrapper;

   type Token_TDH_Getter is access function
     (Token : Token_Reference) return Token_Data_Handler_Access;
   Get_Token_TDH : Token_TDH_Getter;

   type Token_Index_Getter is access function
     (Token : Token_Reference) return Token_Or_Trivia_Index;
   Get_Token_Index : Token_Index_Getter;

   type Token_Text_Extractor is access procedure
     (Token         : Token_Data_Type;
      Source_Buffer : out Text_Cst_Access;
      First         : out Positive;
      Last          : out Natural);
   Extract_Token_Text : Token_Text_Extractor;

end Librflxlang.Private_Converters;
