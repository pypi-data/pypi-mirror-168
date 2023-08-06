






import argparse
import sys
from typing import (
    Any, AnyStr, Callable, ClassVar, Dict, IO, Iterator, List, Optional as Opt,
    Tuple, Type, TypeVar, Union
)





class AnalysisUnitKind(object):
    """
    Specify a kind of analysis unit. Specification units provide an interface
    to the outer world while body units provide an implementation for the
    corresponding interface.
    """
    unit_specification: str
    unit_body: str
class LookupKind(object):
    """
    """
    recursive: str
    flat: str
    minimal: str
class GrammarRule(object):
    """
    Gramar rule to use for parsing.
    """
    main_rule_rule: str
    unqualified_identifier_rule: str
    qualified_identifier_rule: str
    numeric_literal_rule: str
    variable_rule: str
    sequence_aggregate_rule: str
    string_literal_rule: str
    concatenation_rule: str
    primary_rule: str
    paren_expression_rule: str
    suffix_rule: str
    factor_rule: str
    term_rule: str
    unop_term_rule: str
    simple_expr_rule: str
    relation_rule: str
    expression_rule: str
    quantified_expression_rule: str
    comprehension_rule: str
    call_rule: str
    conversion_rule: str
    null_message_aggregate_rule: str
    message_aggregate_association_rule: str
    message_aggregate_association_list_rule: str
    message_aggregate_rule: str
    extended_primary_rule: str
    extended_paren_expression_rule: str
    extended_choice_list_rule: str
    extended_choices_rule: str
    extended_case_expression_rule: str
    extended_suffix_rule: str
    extended_factor_rule: str
    extended_term_rule: str
    extended_unop_term_rule: str
    extended_simple_expr_rule: str
    extended_relation_rule: str
    extended_expression_rule: str
    aspect_rule: str
    range_type_definition_rule: str
    modular_type_definition_rule: str
    integer_type_definition_rule: str
    if_condition_rule: str
    extended_if_condition_rule: str
    then_rule: str
    type_argument_rule: str
    null_message_field_rule: str
    message_field_rule: str
    message_field_list_rule: str
    value_range_rule: str
    checksum_association_rule: str
    checksum_aspect_rule: str
    byte_order_aspect_rule: str
    message_aspect_list_rule: str
    message_type_definition_rule: str
    positional_enumeration_rule: str
    element_value_association_rule: str
    named_enumeration_rule: str
    enumeration_aspects_rule: str
    enumeration_type_definition_rule: str
    type_derivation_definition_rule: str
    sequence_type_definition_rule: str
    type_declaration_rule: str
    type_refinement_rule: str
    parameter_rule: str
    parameter_list_rule: str
    formal_function_declaration_rule: str
    channel_declaration_rule: str
    session_parameter_rule: str
    renaming_declaration_rule: str
    variable_declaration_rule: str
    declaration_rule: str
    description_aspect_rule: str
    assignment_statement_rule: str
    message_field_assignment_statement_rule: str
    list_attribute_rule: str
    reset_rule: str
    attribute_statement_rule: str
    action_rule: str
    conditional_transition_rule: str
    transition_rule: str
    state_body_rule: str
    state_rule: str
    session_declaration_rule: str
    basic_declaration_rule: str
    basic_declarations_rule: str
    package_declaration_rule: str
    context_item_rule: str
    context_clause_rule: str
    specification_rule: str


default_grammar_rule: str


class BadTypeError(Exception):
    pass
class OutOfBoundsError(Exception):
    pass
class InvalidInput(Exception):
    pass
class InvalidSymbolError(Exception):
    pass
class InvalidUnitNameError(Exception):
    pass
class NativeException(Exception):
    pass
class PreconditionFailure(Exception):
    pass
class PropertyError(Exception):
    pass
class TemplateArgsError(Exception):
    pass
class TemplateFormatError(Exception):
    pass
class TemplateInstantiationError(Exception):
    pass
class StaleReferenceError(Exception):
    pass
class UnknownCharset(Exception):
    pass






class AnalysisContext(object):
    """
    This type represents a context for all source analysis. This is the first
    type you need to create to use Librflxlang. It will contain the results of
    all analysis, and is the main holder for all the data.

    You can create several analysis contexts if you need to, which enables you,
    for example to:

    * analyze several different projects at the same time;

    * analyze different parts of the same projects in parallel.

    In the current design, contexts always keep all of their analysis units
    allocated. If you need to get this memory released, the only option at your
    disposal is to destroy your analysis context instance.
    """

    def __init__(self,
                 charset: Opt[str] = None,
                 file_reader: Opt[FileReader] = None,
                 unit_provider: Opt[UnitProvider] = None,
                 with_trivia: bool = True,
                 tab_stop: int = 8,
                 *,
                 _c_value: Any = None) -> None:
        """
        Create a new analysis context.

        ``Charset`` will be used as a default charset to decode input sources
        in analysis units. Please see ``GNATCOLL.Iconv`` for several supported
        charsets. Be careful: passing an unsupported charset is not guaranteed
        to raise an error here. If no charset is provided, ``"utf-8"`` is the
        default.

        .. todo:: Passing an unsupported charset here is not guaranteed to
        raise an error right here, but this would be really helpful for users.

        When ``With_Trivia`` is true, the parsed analysis units will contain
        trivias.

        If provided, ``File_Reader`` will be used to fetch the contents of
        source files instead of the default, which is to just read it from the
        filesystem and decode it using the regular charset rules. Note that if
        provided, all parsing APIs that provide a buffer are forbidden, and any
        use of the rewriting API with the returned context is rejected.

        If provided, ``Unit_Provider`` will be used to query the file name that
        corresponds to a unit reference during semantic analysis. If it is
        ``None``, the default one is used instead.

        ``Tab_Stop`` is a positive number to describe the effect of tabulation
        characters on the column number in source files.
        """

    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...

    def get_from_file(self,
                      filename: AnyStr,
                      charset: Opt[str] = None,
                      reparse: bool = False,
                      rule: str = default_grammar_rule) -> AnalysisUnit:
        """
        Create a new analysis unit for ``Filename`` or return the existing one
        if any. If ``Reparse`` is true and the analysis unit already exists,
        reparse it from ``Filename``.

        ``Rule`` controls which grammar rule is used to parse the unit.

        Use ``Charset`` in order to decode the source. If ``Charset`` is empty
        then use the context's default charset.

        If any failure occurs, such as file opening, decoding, lexing or
        parsing failure, return an analysis unit anyway: errors are described
        as diagnostics of the returned analysis unit.
        """

    def get_from_buffer(self,
                        filename: AnyStr,
                        buffer: AnyStr,
                        charset: Opt[str] = None,
                        reparse: bool = False,
                        rule: str = default_grammar_rule) -> AnalysisUnit:
        """
        Create a new analysis unit for ``Filename`` or return the existing one
        if any. Whether the analysis unit already exists or not, (re)parse it
        from the source code in ``Buffer``.

        ``Rule`` controls which grammar rule is used to parse the unit.

        Use ``Charset`` in order to decode the source. If ``Charset`` is empty
        then use the context's default charset.

        If any failure occurs, such as file opening, decoding, lexing or
        parsing failure, return an analysis unit anyway: errors are described
        as diagnostics of the returned analysis unit.
        """

    def get_from_provider(
        self,
        name: AnyStr,
        kind: str,
        charset: Opt[str] = None,
        reparse: bool = False
    ) -> AnalysisUnit:
        """
        Create a new analysis unit for ``Name``/``Kind`` or return the existing
        one if any. If ``Reparse`` is true and the analysis unit already
        exists, reparse it from ``Filename``.

        Use ``Charset`` in order to decode the source. If ``Charset`` is empty
        then use the context's default charset.

        If the unit name cannot be tuned into a file name, raise an
        ``InvalidUnitNameError`` exception. If any other failure occurs, such
        as file opening, decoding, lexing or parsing failure, return an
        analysis unit anyway: errors are described as diagnostics of the
        returned analysis unit.
        """

    def discard_errors_in_populate_lexical_env(self,
                                               discard: bool) -> None:
        """
        Debug helper. Set whether ``Property_Error`` exceptions raised in
        ``Populate_Lexical_Env`` should be discarded. They are by default.
        """

class AnalysisUnit(object):
    """
    This type represents the analysis of a single file.
    """

    class TokenIterator(object):
        """
        Iterator over the tokens in an analysis unit.
        """

        def __init__(self, first: Token) -> None: ...
        def __iter__(self) -> AnalysisUnit.TokenIterator: ...
        def __next__(self) -> Token: ...
        def next(self) -> Token: ...

    def __init__(self, context: AnalysisContext, c_value: Any) -> None: ...

    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...

    @property
    def context(self) -> AnalysisContext:
        """
        Return the context that owns this unit.
        """

    def reparse(self,
                buffer: Opt[AnyStr] = None,
                charset: Opt[str] = None) -> None:
        """
        Reparse an analysis unit from a buffer, if provided, or from the
        original file otherwise. If ``Charset`` is empty or ``None``, use the
        last charset successfuly used for this unit, otherwise use it to decode
        the content of the source file.

        If any failure occurs, such as decoding, lexing or parsing failure,
        diagnostic are emitted to explain what happened.
        """

    def populate_lexical_env(self) -> None:
        """
        Create lexical environments for this analysis unit, according to the
        specifications given in the language spec.

        If not done before, it will be automatically called during semantic
        analysis. Calling it before enables one to control where the latency
        occurs.

        Depending on whether errors are discarded (see
        ``Discard_Errors_In_Populate_Lexical_Env``), raise a ``Property_Error``
        on failure.
        """

    @property
    def root(self) -> RFLXNode:
        """
        Return the root node for this unit, or ``None`` if there is none.

        :rtype: RFLXNode
        """

    @property
    def first_token(self) -> Token:
        """
        Return a reference to the first token scanned in this unit.
        """

    @property
    def last_token(self) -> Token:
        """
        Return a reference to the last token scanned in this unit.
        """

    @property
    def text(self) -> str:
        """
        Return the source buffer associated to this unit.
        """

    @property
    def token_count(self) -> int:
        """
        Return the number of tokens in this unit.
        """

    @property
    def trivia_count(self) -> int:
        """
        Return the number of trivias in this unit. This is 0 for units that
        were parsed with trivia analysis disabled.
        """

    def lookup_token(self, sloc: Sloc) -> Token:
        """
        Look for a token in this unit that contains the given source location.
        If this falls before the first token, return the first token. If this
        falls between two tokens, return the token that appears before. If this
        falls after the last token, return the last token. If there is no token
        in this unit, return no token.
        """

    def iter_tokens(self) -> AnalysisUnit.TokenIterator:
        """
        Iterator over the tokens in an analysis unit.
        """

    @property
    def filename(self) -> str:
        """
        Return the filename this unit is associated to.
        """

    @property
    def diagnostics(self) -> List[Diagnostic]:
        """
        Diagnostics for this unit.
        """

    def __repr__(self) -> str: ...


class Sloc(object):
    """
    Location in a source file. Line and column numbers are one-based.
    """

    line: int
    column: int

    def __init__(self, line: int, column: int) -> None: ...
    def __bool__(self) -> bool: ...
    def __nonzero__(self) -> bool: ...
    def __lt__(self, other: Sloc) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class SlocRange(object):
    """
    Location of a span of text in a source file.
    """

    start: Sloc
    end: Sloc

    def __init__(self, start: Sloc, end: Sloc) -> None: ...
    def __bool__(self) -> bool: ...
    def __nonzero__(self) -> bool: ...
    def __lt__(self, other: SlocRange) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class Diagnostic(object):
    """
    Diagnostic for an analysis unit: cannot open the source file, parsing
    error, ...
    """

    sloc_range: SlocRange
    message: str

    def __init__(self, sloc_range: SlocRange, message: str) -> None: ...

    @property
    def as_text(self) -> str: ...

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class Token(object):
    """
    Reference to a token in an analysis unit.
    """

    @property
    def next(self) -> Opt[Token]:
        """
        Return a reference to the next token in the corresponding analysis
        unit.
        """

    @property
    def previous(self) -> Opt[Token]:
        """
        Return a reference to the previous token in the corresponding analysis
        unit.
        """

    def range_until(self, other: Token) -> Iterator[Token]:
        """
        Return an iterator on the list of tokens that spans between `self` and
        `other` (included). This returns an empty list if the first token
        appears after the other one in the source code. Raise a ``ValueError``
        if both tokens come from different analysis units.
        """

    def is_equivalent(self, other: Token) -> bool:
        """
        Return whether ``L`` and ``R`` are structurally equivalent tokens. This
        means that their position in the stream won't be taken into account,
        only the kind and text of the token.
        """

    @property
    def kind(self) -> str:
        """
        Kind for this token.
        """

    @property
    def is_trivia(self) -> bool:
        """
        Return whether this token is a trivia. If it's not, it's a regular
        token.
        """

    @property
    def index(self) -> int:
        """
        Zero-based index for this token/trivia. Tokens and trivias get their
        own index space.
        """

    @property
    def text(self) -> str:
        """
        Return the text of the given token.
        """

    @classmethod
    def text_range(cls, first: Token, last: Token) -> str:
        """
        Compute the source buffer slice corresponding to the text that spans
        between the ``First`` and ``Last`` tokens (both included). This yields
        an empty slice if ``Last`` actually appears before ``First``.

        This raises a ``ValueError`` if ``First`` and ``Last`` don't belong to
        the same analysis unit.
        """

    @property
    def sloc_range(self) -> SlocRange:
        """
        Return the source location range of the given token.
        """

    def __eq__(self, other: Any) -> bool:
        """
        Return whether the two tokens refer to the same token in the same unit.

        Note that this does not actually compares the token data.
        """

    def __hash__(self) -> int: ...
    def __repr__(self) -> str: ...

    def __lt__(self, other: Opt[Token]) -> bool:
        """
        Consider that None comes before all tokens. Then, sort by unit, token
        index, and trivia index.
        """

    def __le__(self, other: Opt[Token]) -> bool: ...
    def __gt__(self, other: Opt[Token]) -> bool: ...
    def __ge__(self, other: Opt[Token]) -> bool: ...

    def to_data(self) -> dict:
        """
        Return a dict representation of this Token.
        """


class FileReader(object):
    """
    Interface to override how source files are fetched and decoded.
    """

    def __init__(self, c_value: Any) -> None:
        """
        This constructor is an implementation detail, and is not meant to be
        used directly.
        """





class UnitProvider(object):
    """
    Interface to fetch analysis units from a name and a unit kind.

    The unit provider mechanism provides an abstraction which assumes that to
    any couple (unit name, unit kind) we can associate at most one source file.
    This means that several couples can be associated to the same source file,
    but on the other hand, only one one source file can be associated to a
    couple.

    This is used to make the semantic analysis able to switch from one analysis
    units to another.
    """

    def __init__(self, c_value: Any) -> None:
        """
        This constructor is an implementation detail, and is not meant to be
        used directly.
        """





class RFLXNode(object):
    """
    Root node class for the RecordFlux language.
    """

    is_list_type: ClassVar[bool]

    
    

    
    @property
    def parent(
        self
    ) -> RFLXNode:
        """
        Return the lexical parent for this node. Return null for the root AST
        node or for AST nodes for which no one has a reference to the parent.
        """
    
    def parents(
        self, with_self: bool = True
    ) -> List[RFLXNode]:
        """
        Return an array that contains the lexical parents, this node included
        iff ``with_self`` is True. Nearer parents are first in the list.
        """
    
    @property
    def children(
        self
    ) -> List[RFLXNode]:
        """
        Return an array that contains the direct lexical children.
        """
    
    @property
    def token_start(
        self
    ) -> Token:
        """
        Return the first token used to parse this node.
        """
    
    @property
    def token_end(
        self
    ) -> Token:
        """
        Return the last token used to parse this node.
        """
    
    @property
    def child_index(
        self
    ) -> int:
        """
        Return the 0-based index for Node in its parent's children.
        """
    
    @property
    def previous_sibling(
        self
    ) -> RFLXNode:
        """
        Return the node's previous sibling, if there is one.
        """
    
    @property
    def next_sibling(
        self
    ) -> RFLXNode:
        """
        Return the node's next sibling, if there is one.
        """
    
    @property
    def unit(
        self
    ) -> AnalysisUnit:
        """
        Return the analysis unit owning this node.
        """
    
    @property
    def is_ghost(
        self
    ) -> bool:
        """
        Return whether the node is a ghost.

        Unlike regular nodes, ghost nodes cover no token in the input source:
        they are logically located instead between two tokens. The
        "token_first" of all ghost nodes is the token right after this logical
        position, while they have no "token_last".
        """
    
    @property
    def full_sloc_image(
        self
    ) -> str:
        """
        Return a string containing the filename + the sloc in GNU conformant
        format. Useful to create diagnostics from a node.
        """





    def __init__(self,
                 c_value: Any,
                 node_c_value: Any,
                 metadata: Any,
                 rebindings: Any) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...

    @property
    def kind_name(self) -> str:
        """
        Return the kind of this node.
        """

    @property
    def is_token_node(self) -> bool:
        """
        Return whether this node is a node that contains only a single token.
        """

    @property
    def is_synthetic(self) -> bool:
        """
        Return whether this node is synthetic.
        """

    @property
    def sloc_range(self) -> SlocRange:
        """
        Return the spanning source location range for this node.

        Note that this returns the sloc of the parent for synthetic nodes.
        """

    @property
    def text(self) -> str:
        """
        Return the source buffer slice corresponding to the text that spans
        between the first and the last tokens of this node.

        Note that this returns the empty string for synthetic nodes.
        """

    @property
    def image(self) -> str:
        """
        Return a representation of this node as a string.
        """

    def lookup(self, sloc: Sloc) -> Opt[RFLXNode]:
        """
        Return the bottom-most node from in ``Node`` and its children which
        contains ``Sloc``, or ``None`` if there is none.
        """

    def __bool__(self) -> bool:
        """
        Return always True so that checking a node against None can be done as
        simply as::

        if node: ...
        """

    def __nonzero__(self) -> bool: ...

    def __iter__(self) -> Iterator[RFLXNode]:
        """
        Return an iterator on the children of this node.
        """

    def __len__(self) -> int:
        """
        Return the number of RFLXNode children this node has.
        """

    def __getitem__(self, key: int) -> Opt[RFLXNode]:
        """
        Return the Nth RFLXNode child this node has.

        This handles negative indexes the same way Python lists do. Raise an
        IndexError if "key" is out of range.
        """

    def iter_fields(self) -> Iterator[Tuple[str, RFLXNode]]:
        """
        Iterate through all the fields this node contains.

        Return an iterator that yields (name, value) couples for all abstract
        fields in this node. If "self" is a list, field names will be
        "item_{n}" with "n" being the index.
        """

    def dump_str(self) -> str:
        """
        Dump the sub-tree to a string in a human-readable format.
        """

    def dump(self, indent: str = '', file: IO[str] = sys.stdout) -> None:
        """
        Dump the sub-tree in a human-readable format on the given file.

        :param str indent: Prefix printed on each line during the dump. :param
        file file: File in which the dump must occur.
        """

    def findall(
        self,
        ast_type_or_pred: Union[Type[RFLXNode],
                                Callable[[RFLXNode], bool]],
        **kwargs: Any
    ) -> List[RFLXNode]:
        """
        Helper for finditer that will return all results as a list. See
        finditer's documentation for more details.
        """

    def find(
        self,
        ast_type_or_pred: Union[Type[RFLXNode],
                                Callable[[RFLXNode], bool]],
        **kwargs: Any
    ) -> Opt[RFLXNode]:
        """
        Helper for finditer that will return only the first result. See
        finditer's documentation for more details.
        """

    def finditer(
        self,
        ast_type_or_pred: Union[Type[RFLXNode],
                                Callable[[RFLXNode], bool]],
        **kwargs: Any
    ) -> Iterator[RFLXNode]:
        """
        Find every node corresponding to the passed predicates.

        :param ast_type_or_pred: If supplied with a subclass of RFLXNode, will
        constrain the resulting collection to only the instances of this type
        or any subclass. If supplied with a predicate, it will apply the
        predicate on every node and keep only the ones for which it returns
        True. If supplied with a list of subclasses of RFLXNode, it will match
        all instances of any of them. :type ast_type_or_pred: type|((RFLXNode)
        -> bool)|list[type]

        :param kwargs: Allows the user to filter on attributes of the node. For
        every key value association, if the node has an attribute of name key
        that has the specified value, then the child is kept. :type kwargs:
        dict[str, Any]
        """

    @property
    def parent_chain(self) -> List[RFLXNode]:
        """
        Return the parent chain of self. Self will be the first element,
        followed by the first parent, then this parent's parent, etc.
        """

    def __repr__(self) -> str: ...

    @property
    def entity_repr(self) -> str: ...

    @property
    def tokens(self) -> Iterator[Token]:
        """
        Return an iterator on the range of tokens that self encompasses.
        """

    def to_data(self) -> Union[list, dict]:
        """
        Return a nested python data-structure, constituted only of standard
        data types (dicts, lists, strings, ints, etc), and representing the
        portion of the AST corresponding to this node.
        """

    def to_json(self) -> str:
        """
        Return a JSON representation of this node.
        """

    def is_a(self, *types: Type[RFLXNode]) -> bool:
        """
        Shortcut for isinstance(self, types). :rtype: bool
        """

    T = TypeVar('T', bound=RFLXNode)

    def cast(self, typ: Type[T]) -> T:
        """
        Fluent interface style method. Return ``self``, raise an error if self
        is not of type ``typ``.

        :type typ: () -> T :rtype: T
        """



class AbstractID(RFLXNode):
    """
    Base class for identifiers.
    """

    



    pass





class ID(AbstractID):
    """
    Qualified identifiers which may optionally have a package part (e.g.
    "Pkg::Foo", "Foo").
    """

    

    
    @property
    def f_package(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_name(
        self
    ) -> UnqualifiedID:
        pass







class UnqualifiedID(AbstractID):
    """
    Simple, unqualified identifiers, i.e. identifiers without a package part
    (e.g. "Foo").
    """

    



    pass





class Aspect(RFLXNode):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_value(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """







class Attr(RFLXNode):
    """
    Attribute kind.
    """

    



    pass





class AttrFirst(Attr):
    """
    """

    



    pass





class AttrHasData(Attr):
    """
    """

    



    pass





class AttrHead(Attr):
    """
    """

    



    pass





class AttrLast(Attr):
    """
    """

    



    pass





class AttrOpaque(Attr):
    """
    """

    



    pass





class AttrPresent(Attr):
    """
    """

    



    pass





class AttrSize(Attr):
    """
    """

    



    pass





class AttrValid(Attr):
    """
    """

    



    pass





class AttrValidChecksum(Attr):
    """
    """

    



    pass





class AttrStmt(RFLXNode):
    """
    Attribute statement kind.
    """

    



    pass





class AttrStmtAppend(AttrStmt):
    """
    """

    



    pass





class AttrStmtExtend(AttrStmt):
    """
    """

    



    pass





class AttrStmtRead(AttrStmt):
    """
    """

    



    pass





class AttrStmtWrite(AttrStmt):
    """
    """

    



    pass





class BaseAggregate(RFLXNode):
    """
    Base class for message aggregates.
    """

    



    pass





class MessageAggregateAssociations(BaseAggregate):
    """
    """

    

    
    @property
    def f_associations(
        self
    ) -> MessageAggregateAssociationList:
        pass







class NullMessageAggregate(BaseAggregate):
    """
    """

    



    pass





class BaseChecksumVal(RFLXNode):
    """
    Base class for checksum values.
    """

    



    pass





class ChecksumVal(BaseChecksumVal):
    """
    Single checksum value.
    """

    

    
    @property
    def f_data(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """







class ChecksumValueRange(BaseChecksumVal):
    """
    Checksum value range.
    """

    

    
    @property
    def f_first(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_last(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """







class ByteOrderType(RFLXNode):
    """
    """

    



    pass





class ByteOrderTypeHighorderfirst(ByteOrderType):
    """
    """

    



    pass





class ByteOrderTypeLoworderfirst(ByteOrderType):
    """
    """

    



    pass





class ChannelAttribute(RFLXNode):
    """
    Base class for channel attributes.
    """

    



    pass





class Readable(ChannelAttribute):
    """
    Channel attribute (channel can be read).
    """

    



    pass





class Writable(ChannelAttribute):
    """
    Channel attribute (channel can be written).
    """

    



    pass





class ChecksumAssoc(RFLXNode):
    """
    Association between checksum field and list of covered fields.
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_covered_fields(
        self
    ) -> BaseChecksumValList:
        pass







class Declaration(RFLXNode):
    """
    Base class for declarations (types, refinements, sessions).
    """

    



    pass





class RefinementDecl(Declaration):
    """
    Refinement declaration (for Message use (Field => Inner_Type)).
    """

    

    
    @property
    def f_pdu(
        self
    ) -> ID:
        pass
    
    @property
    def f_field(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_sdu(
        self
    ) -> ID:
        pass
    
    @property
    def f_condition(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """







class SessionDecl(Declaration):
    """
    """

    

    
    @property
    def f_parameters(
        self
    ) -> FormalDeclList:
        pass
    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_declarations(
        self
    ) -> LocalDeclList:
        pass
    
    @property
    def f_states(
        self
    ) -> StateList:
        pass
    
    @property
    def f_end_identifier(
        self
    ) -> UnqualifiedID:
        pass







class TypeDecl(Declaration):
    """
    Type declaration (type Foo is ...).
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_parameters(
        self
    ) -> Parameters:
        pass
    
    @property
    def f_definition(
        self
    ) -> TypeDef:
        """
        This field can contain one of the following nodes:

        * AbstractMessageTypeDef

        * EnumerationTypeDef

        * IntegerTypeDef

        * SequenceTypeDef

        * TypeDerivationDef
        """







class Description(RFLXNode):
    """
    String description of an entity.
    """

    

    
    @property
    def f_content(
        self
    ) -> StringLiteral:
        pass







class ElementValueAssoc(RFLXNode):
    """
    Element/value association.
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_literal(
        self
    ) -> NumericLiteral:
        pass







class Expr(RFLXNode):
    """
    Base class for expressions.
    """

    



    pass





class Attribute(Expr):
    """
    """

    

    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_kind(
        self
    ) -> Attr:
        pass







class BinOp(Expr):
    """
    Binary operation.
    """

    

    
    @property
    def f_left(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_op(
        self
    ) -> Op:
        pass
    
    @property
    def f_right(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class Binding(Expr):
    """
    """

    

    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_bindings(
        self
    ) -> TermAssocList:
        pass







class Call(Expr):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_arguments(
        self
    ) -> ExprList:
        """
        This field contains a list that itself contains one of the following
        nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class CaseExpression(Expr):
    """
    """

    

    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_choices(
        self
    ) -> ChoiceList:
        pass







class Choice(Expr):
    """
    """

    

    
    @property
    def f_selectors(
        self
    ) -> RFLXNodeList:
        """
        This field contains a list that itself contains one of the following
        nodes:

        * ID

        * NumericLiteral
        """
    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class Comprehension(Expr):
    """
    """

    

    
    @property
    def f_iterator(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_sequence(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_condition(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_selector(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class ContextItem(Expr):
    """
    Import statement (with Package).
    """

    

    
    @property
    def f_item(
        self
    ) -> UnqualifiedID:
        pass







class Conversion(Expr):
    """
    """

    

    
    @property
    def f_target_identifier(
        self
    ) -> ID:
        pass
    
    @property
    def f_argument(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class MessageAggregate(Expr):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> ID:
        pass
    
    @property
    def f_values(
        self
    ) -> BaseAggregate:
        pass







class Negation(Expr):
    """
    """

    

    
    @property
    def f_data(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class NumericLiteral(Expr):
    """
    """

    



    pass





class ParenExpression(Expr):
    """
    Parenthesized expression.
    """

    

    
    @property
    def f_data(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class QuantifiedExpression(Expr):
    """
    """

    

    
    @property
    def f_operation(
        self
    ) -> Quantifier:
        pass
    
    @property
    def f_parameter_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_iterable(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_predicate(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class SelectNode(Expr):
    """
    """

    

    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_selector(
        self
    ) -> UnqualifiedID:
        pass







class SequenceLiteral(Expr):
    """
    Base class for sequence literals (strings, sequence aggregates).
    """

    



    pass





class Concatenation(SequenceLiteral):
    """
    Concatenation of aggregates or string literals.
    """

    

    
    @property
    def f_left(
        self
    ) -> SequenceLiteral:
        pass
    
    @property
    def f_right(
        self
    ) -> SequenceLiteral:
        """
        This field can contain one of the following nodes:

        * SequenceAggregate

        * StringLiteral
        """







class SequenceAggregate(SequenceLiteral):
    """
    List of literal sequence values.
    """

    

    
    @property
    def f_values(
        self
    ) -> NumericLiteralList:
        pass







class StringLiteral(SequenceLiteral):
    """
    Double-quoted string literal.
    """

    



    pass





class Variable(Expr):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> ID:
        pass







class FormalDecl(RFLXNode):
    """
    Base class for generic formal session declarations.
    """

    



    pass





class FormalChannelDecl(FormalDecl):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_parameters(
        self
    ) -> ChannelAttributeList:
        pass







class FormalFunctionDecl(FormalDecl):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_parameters(
        self
    ) -> Parameters:
        pass
    
    @property
    def f_return_type_identifier(
        self
    ) -> ID:
        pass







class LocalDecl(RFLXNode):
    """
    Base class for session or state local declarations.
    """

    



    pass





class RenamingDecl(LocalDecl):
    """
    Session renaming declaration.
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_type_identifier(
        self
    ) -> ID:
        pass
    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class VariableDecl(LocalDecl):
    """
    Session variable declaration.
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_type_identifier(
        self
    ) -> ID:
        pass
    
    @property
    def f_initializer(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class MessageAggregateAssociation(RFLXNode):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class MessageAspect(RFLXNode):
    """
    Base class for message aspects.
    """

    



    pass





class ByteOrderAspect(MessageAspect):
    """
    """

    

    
    @property
    def f_byte_order(
        self
    ) -> ByteOrderType:
        pass







class ChecksumAspect(MessageAspect):
    """
    """

    

    
    @property
    def f_associations(
        self
    ) -> ChecksumAssocList:
        pass







class MessageField(RFLXNode):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_type_identifier(
        self
    ) -> ID:
        pass
    
    @property
    def f_type_arguments(
        self
    ) -> TypeArgumentList:
        pass
    
    @property
    def f_aspects(
        self
    ) -> AspectList:
        pass
    
    @property
    def f_condition(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_thens(
        self
    ) -> ThenNodeList:
        pass







class MessageFields(RFLXNode):
    """
    """

    

    
    @property
    def f_initial_field(
        self
    ) -> NullMessageField:
        pass
    
    @property
    def f_fields(
        self
    ) -> MessageFieldList:
        pass







class NullMessageField(RFLXNode):
    """
    """

    

    
    @property
    def f_then(
        self
    ) -> ThenNode:
        pass







class Op(RFLXNode):
    """
    Operators for binary expressions.
    """

    



    pass





class OpAdd(Op):
    """
    """

    



    pass





class OpAnd(Op):
    """
    """

    



    pass





class OpDiv(Op):
    """
    """

    



    pass





class OpEq(Op):
    """
    """

    



    pass





class OpGe(Op):
    """
    """

    



    pass





class OpGt(Op):
    """
    """

    



    pass





class OpIn(Op):
    """
    """

    



    pass





class OpLe(Op):
    """
    """

    



    pass





class OpLt(Op):
    """
    """

    



    pass





class OpMod(Op):
    """
    """

    



    pass





class OpMul(Op):
    """
    """

    



    pass





class OpNeq(Op):
    """
    """

    



    pass





class OpNotin(Op):
    """
    """

    



    pass





class OpOr(Op):
    """
    """

    



    pass





class OpPow(Op):
    """
    """

    



    pass





class OpSub(Op):
    """
    """

    



    pass





class PackageNode(RFLXNode):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_declarations(
        self
    ) -> DeclarationList:
        pass
    
    @property
    def f_end_identifier(
        self
    ) -> UnqualifiedID:
        pass







class Parameter(RFLXNode):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_type_identifier(
        self
    ) -> ID:
        pass







class Parameters(RFLXNode):
    """
    """

    

    
    @property
    def f_parameters(
        self
    ) -> ParameterList:
        pass







class Quantifier(RFLXNode):
    """
    Quantifier kind.
    """

    



    pass





class QuantifierAll(Quantifier):
    """
    """

    



    pass





class QuantifierSome(Quantifier):
    """
    """

    



    pass





class RFLXNodeBaseList(RFLXNode):
    """
    """

    



    pass





class AspectList(RFLXNodeBaseList):
    """
    List of Aspect.
    """

    


    def __iter__(self) -> Iterator[Aspect]: ...
    def __getitem__(self,
                    index: int) -> Aspect: ...






class BaseChecksumValList(RFLXNodeBaseList):
    """
    List of BaseChecksumVal.
    """

    


    def __iter__(self) -> Iterator[BaseChecksumVal]: ...
    def __getitem__(self,
                    index: int) -> BaseChecksumVal: ...






class ChannelAttributeList(RFLXNodeBaseList):
    """
    List of ChannelAttribute.
    """

    


    def __iter__(self) -> Iterator[ChannelAttribute]: ...
    def __getitem__(self,
                    index: int) -> ChannelAttribute: ...






class ChecksumAssocList(RFLXNodeBaseList):
    """
    List of ChecksumAssoc.
    """

    


    def __iter__(self) -> Iterator[ChecksumAssoc]: ...
    def __getitem__(self,
                    index: int) -> ChecksumAssoc: ...






class ChoiceList(RFLXNodeBaseList):
    """
    List of Choice.
    """

    


    def __iter__(self) -> Iterator[Choice]: ...
    def __getitem__(self,
                    index: int) -> Choice: ...






class ConditionalTransitionList(RFLXNodeBaseList):
    """
    List of ConditionalTransition.
    """

    


    def __iter__(self) -> Iterator[ConditionalTransition]: ...
    def __getitem__(self,
                    index: int) -> ConditionalTransition: ...






class ContextItemList(RFLXNodeBaseList):
    """
    List of ContextItem.
    """

    


    def __iter__(self) -> Iterator[ContextItem]: ...
    def __getitem__(self,
                    index: int) -> ContextItem: ...






class DeclarationList(RFLXNodeBaseList):
    """
    List of Declaration.
    """

    


    def __iter__(self) -> Iterator[Declaration]: ...
    def __getitem__(self,
                    index: int) -> Declaration: ...






class ElementValueAssocList(RFLXNodeBaseList):
    """
    List of ElementValueAssoc.
    """

    


    def __iter__(self) -> Iterator[ElementValueAssoc]: ...
    def __getitem__(self,
                    index: int) -> ElementValueAssoc: ...






class ExprList(RFLXNodeBaseList):
    """
    List of Expr.

    This list node can contain one of the following nodes:

    * Attribute

    * BinOp

    * Binding

    * Call

    * CaseExpression

    * Comprehension

    * Conversion

    * MessageAggregate

    * Negation

    * NumericLiteral

    * ParenExpression

    * QuantifiedExpression

    * SelectNode

    * SequenceLiteral

    * Variable
    """

    


    def __iter__(self) -> Iterator[Expr]: ...
    def __getitem__(self,
                    index: int) -> Expr: ...






class FormalDeclList(RFLXNodeBaseList):
    """
    List of FormalDecl.
    """

    


    def __iter__(self) -> Iterator[FormalDecl]: ...
    def __getitem__(self,
                    index: int) -> FormalDecl: ...






class LocalDeclList(RFLXNodeBaseList):
    """
    List of LocalDecl.
    """

    


    def __iter__(self) -> Iterator[LocalDecl]: ...
    def __getitem__(self,
                    index: int) -> LocalDecl: ...






class MessageAggregateAssociationList(RFLXNodeBaseList):
    """
    List of MessageAggregateAssociation.
    """

    


    def __iter__(self) -> Iterator[MessageAggregateAssociation]: ...
    def __getitem__(self,
                    index: int) -> MessageAggregateAssociation: ...






class MessageAspectList(RFLXNodeBaseList):
    """
    List of MessageAspect.
    """

    


    def __iter__(self) -> Iterator[MessageAspect]: ...
    def __getitem__(self,
                    index: int) -> MessageAspect: ...






class MessageFieldList(RFLXNodeBaseList):
    """
    List of MessageField.
    """

    


    def __iter__(self) -> Iterator[MessageField]: ...
    def __getitem__(self,
                    index: int) -> MessageField: ...






class NumericLiteralList(RFLXNodeBaseList):
    """
    List of NumericLiteral.
    """

    


    def __iter__(self) -> Iterator[NumericLiteral]: ...
    def __getitem__(self,
                    index: int) -> NumericLiteral: ...






class ParameterList(RFLXNodeBaseList):
    """
    List of Parameter.
    """

    


    def __iter__(self) -> Iterator[Parameter]: ...
    def __getitem__(self,
                    index: int) -> Parameter: ...






class RFLXNodeList(RFLXNodeBaseList):
    """
    List of RFLXNode.

    This list node can contain one of the following nodes:

    * ID

    * NumericLiteral
    """

    


    def __iter__(self) -> Iterator[RFLXNode]: ...
    def __getitem__(self,
                    index: int) -> RFLXNode: ...






class StateList(RFLXNodeBaseList):
    """
    List of State.
    """

    


    def __iter__(self) -> Iterator[State]: ...
    def __getitem__(self,
                    index: int) -> State: ...






class StatementList(RFLXNodeBaseList):
    """
    List of Statement.
    """

    


    def __iter__(self) -> Iterator[Statement]: ...
    def __getitem__(self,
                    index: int) -> Statement: ...






class TermAssocList(RFLXNodeBaseList):
    """
    List of TermAssoc.
    """

    


    def __iter__(self) -> Iterator[TermAssoc]: ...
    def __getitem__(self,
                    index: int) -> TermAssoc: ...






class ThenNodeList(RFLXNodeBaseList):
    """
    List of Then.
    """

    


    def __iter__(self) -> Iterator[ThenNode]: ...
    def __getitem__(self,
                    index: int) -> ThenNode: ...






class TypeArgumentList(RFLXNodeBaseList):
    """
    List of TypeArgument.
    """

    


    def __iter__(self) -> Iterator[TypeArgument]: ...
    def __getitem__(self,
                    index: int) -> TypeArgument: ...






class UnqualifiedIDList(RFLXNodeBaseList):
    """
    List of UnqualifiedID.
    """

    


    def __iter__(self) -> Iterator[UnqualifiedID]: ...
    def __getitem__(self,
                    index: int) -> UnqualifiedID: ...






class Specification(RFLXNode):
    """
    RecordFlux specification.
    """

    

    
    @property
    def f_context_clause(
        self
    ) -> ContextItemList:
        pass
    
    @property
    def f_package_declaration(
        self
    ) -> PackageNode:
        pass







class State(RFLXNode):
    """
    Session state.
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_description(
        self
    ) -> Description:
        pass
    
    @property
    def f_body(
        self
    ) -> StateBody:
        pass







class StateBody(RFLXNode):
    """
    Body of a session state.
    """

    

    
    @property
    def f_declarations(
        self
    ) -> LocalDeclList:
        pass
    
    @property
    def f_actions(
        self
    ) -> StatementList:
        pass
    
    @property
    def f_conditional_transitions(
        self
    ) -> ConditionalTransitionList:
        pass
    
    @property
    def f_final_transition(
        self
    ) -> Transition:
        pass
    
    @property
    def f_exception_transition(
        self
    ) -> Transition:
        pass
    
    @property
    def f_end_identifier(
        self
    ) -> UnqualifiedID:
        pass







class Statement(RFLXNode):
    """
    Base class for statements.
    """

    



    pass





class Assignment(Statement):
    """
    Assignment of expression to unqualified identifier.
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class AttributeStatement(Statement):
    """
    Attribute statement.
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_attr(
        self
    ) -> AttrStmt:
        pass
    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class MessageFieldAssignment(Statement):
    """
    Assignment of expression to message field.
    """

    

    
    @property
    def f_message(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_field(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class Reset(Statement):
    """
    Reset statement.
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_associations(
        self
    ) -> MessageAggregateAssociationList:
        pass







class TermAssoc(RFLXNode):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class ThenNode(RFLXNode):
    """
    Link to field.
    """

    

    
    @property
    def f_target(
        self
    ) -> AbstractID:
        pass
    
    @property
    def f_aspects(
        self
    ) -> AspectList:
        pass
    
    @property
    def f_condition(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """







class Transition(RFLXNode):
    """
    Unconditional session state transition.
    """

    

    
    @property
    def f_target(
        self
    ) -> AbstractID:
        pass
    
    @property
    def f_description(
        self
    ) -> Description:
        pass







class ConditionalTransition(Transition):
    """
    Conditional session state transition.
    """

    

    
    @property
    def f_condition(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Binding

        * Call

        * CaseExpression

        * Comprehension

        * Conversion

        * MessageAggregate

        * Negation

        * NumericLiteral

        * ParenExpression

        * QuantifiedExpression

        * SelectNode

        * SequenceLiteral

        * Variable
        """







class TypeArgument(RFLXNode):
    """
    """

    

    
    @property
    def f_identifier(
        self
    ) -> UnqualifiedID:
        pass
    
    @property
    def f_expression(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """







class TypeDef(RFLXNode):
    """
    Base class for type definitions (integers, messages, type derivations,
    sequences, enums).
    """

    



    pass





class AbstractMessageTypeDef(TypeDef):
    """
    Base class for message type definitions.
    """

    



    pass





class MessageTypeDef(AbstractMessageTypeDef):
    """
    """

    

    
    @property
    def f_message_fields(
        self
    ) -> MessageFields:
        pass
    
    @property
    def f_aspects(
        self
    ) -> MessageAspectList:
        pass







class NullMessageTypeDef(AbstractMessageTypeDef):
    """
    """

    



    pass





class EnumerationDef(TypeDef):
    """
    Base class for enumeration definitions.
    """

    



    pass





class NamedEnumerationDef(EnumerationDef):
    """
    """

    

    
    @property
    def f_elements(
        self
    ) -> ElementValueAssocList:
        pass







class PositionalEnumerationDef(EnumerationDef):
    """
    """

    

    
    @property
    def f_elements(
        self
    ) -> UnqualifiedIDList:
        pass







class EnumerationTypeDef(TypeDef):
    """
    """

    

    
    @property
    def f_elements(
        self
    ) -> EnumerationDef:
        pass
    
    @property
    def f_aspects(
        self
    ) -> AspectList:
        pass







class IntegerTypeDef(TypeDef):
    """
    Base class for all integer type definitions.
    """

    



    pass





class ModularTypeDef(IntegerTypeDef):
    """
    """

    

    
    @property
    def f_mod(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """







class RangeTypeDef(IntegerTypeDef):
    """
    """

    

    
    @property
    def f_first(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_last(
        self
    ) -> Expr:
        """
        This field can contain one of the following nodes:

        * Attribute

        * BinOp

        * Negation

        * NumericLiteral

        * ParenExpression

        * SequenceLiteral

        * Variable
        """
    
    @property
    def f_size(
        self
    ) -> Aspect:
        pass







class SequenceTypeDef(TypeDef):
    """
    """

    

    
    @property
    def f_element_type(
        self
    ) -> ID:
        pass







class TypeDerivationDef(TypeDef):
    """
    """

    

    
    @property
    def f_base(
        self
    ) -> ID:
        pass











version: str
build_date: str






class App(object):
    parser: argparse.ArgumentParser
    args: argparse.Namespace
    u: AnalysisUnit
    units: Dict[str, AnalysisUnit]
    ctx: AnalysisContext

    @property
    def description(self) -> str: ...

    def __init__(self, args: Opt[List[str]]) -> None: ...
    def add_arguments(self) -> None: ...
    def create_unit_provider(self) -> Opt[UnitProvider]: ...
    def process_unit(self, unit: AnalysisUnit) -> None: ...

    @classmethod
    def run(cls, args: Opt[List[str]]=None) -> None: ...

    

