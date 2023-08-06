/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Declarations                                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#if defined(GET_OP_CLASSES) || defined(GET_OP_FWD_DEFINES)
#undef GET_OP_FWD_DEFINES
namespace mlir {
namespace pdl {
class ApplyNativeConstraintOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class ApplyNativeRewriteOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class AttributeOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class EraseOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class OperandOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class OperandsOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class OperationOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class PatternOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class ReplaceOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class ResultOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class ResultsOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class RewriteOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class TypeOp;
} // namespace pdl
} // namespace mlir
namespace mlir {
namespace pdl {
class TypesOp;
} // namespace pdl
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::ApplyNativeConstraintOp declarations
//===----------------------------------------------------------------------===//

class ApplyNativeConstraintOpAdaptor {
public:
  ApplyNativeConstraintOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ApplyNativeConstraintOpAdaptor(ApplyNativeConstraintOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getArgs();
  ::mlir::ValueRange args();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getNameAttr();
  ::llvm::StringRef getName();
  ::mlir::StringAttr nameAttr();
  ::llvm::StringRef name();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class ApplyNativeConstraintOp : public ::mlir::Op<ApplyNativeConstraintOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::HasParent<pdl::PatternOp>::Impl, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ApplyNativeConstraintOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("name")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getNameAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr nameAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.apply_native_constraint");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getArgs();
  ::mlir::Operation::operand_range args();
  ::mlir::MutableOperandRange getArgsMutable();
  ::mlir::MutableOperandRange argsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::StringAttr getNameAttr();
  ::llvm::StringRef getName();
  ::mlir::StringAttr nameAttr();
  ::llvm::StringRef name();
  void setNameAttr(::mlir::StringAttr attr);
  void nameAttr(::mlir::StringAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::StringAttr name, ::mlir::ValueRange args);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::StringAttr name, ::mlir::ValueRange args);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::llvm::StringRef name, ::mlir::ValueRange args);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::llvm::StringRef name, ::mlir::ValueRange args);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::ApplyNativeConstraintOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::ApplyNativeRewriteOp declarations
//===----------------------------------------------------------------------===//

class ApplyNativeRewriteOpAdaptor {
public:
  ApplyNativeRewriteOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ApplyNativeRewriteOpAdaptor(ApplyNativeRewriteOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getArgs();
  ::mlir::ValueRange args();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getNameAttr();
  ::llvm::StringRef getName();
  ::mlir::StringAttr nameAttr();
  ::llvm::StringRef name();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class ApplyNativeRewriteOp : public ::mlir::Op<ApplyNativeRewriteOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::HasParent<pdl::RewriteOp>::Impl, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ApplyNativeRewriteOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("name")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getNameAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr nameAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.apply_native_rewrite");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getArgs();
  ::mlir::Operation::operand_range args();
  ::mlir::MutableOperandRange getArgsMutable();
  ::mlir::MutableOperandRange argsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getResults();
  ::mlir::Operation::result_range results();
  ::mlir::StringAttr getNameAttr();
  ::llvm::StringRef getName();
  ::mlir::StringAttr nameAttr();
  ::llvm::StringRef name();
  void setNameAttr(::mlir::StringAttr attr);
  void nameAttr(::mlir::StringAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::mlir::StringAttr name, ::mlir::ValueRange args);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::llvm::StringRef name, ::mlir::ValueRange args);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::ApplyNativeRewriteOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::AttributeOp declarations
//===----------------------------------------------------------------------===//

class AttributeOpAdaptor {
public:
  AttributeOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  AttributeOpAdaptor(AttributeOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getValueType();
  ::mlir::Value valueType();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::Attribute getValueAttr();
  ::llvm::Optional<::mlir::Attribute> getValue();
  ::mlir::Attribute valueAttr();
  ::llvm::Optional<::mlir::Attribute> value();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class AttributeOp : public ::mlir::Op<AttributeOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::pdl::AttributeType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = AttributeOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("value")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getValueAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getValueAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr valueAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr valueAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.attribute");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getValueType();
  ::mlir::Value valueType();
  ::mlir::MutableOperandRange getValueTypeMutable();
  ::mlir::MutableOperandRange valueTypeMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::AttributeType> getAttr();
  ::mlir::TypedValue<::mlir::pdl::AttributeType> attr();
  ::mlir::Attribute getValueAttr();
  ::llvm::Optional<::mlir::Attribute> getValue();
  ::mlir::Attribute valueAttr();
  ::llvm::Optional<::mlir::Attribute> value();
  void setValueAttr(::mlir::Attribute attr);
  void valueAttr(::mlir::Attribute attr);
  ::mlir::Attribute removeValueAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, Value type = Value());
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, Attribute attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type attr, /*optional*/::mlir::Value valueType, /*optional*/::mlir::Attribute value);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::Value valueType, /*optional*/::mlir::Attribute value);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::AttributeOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::EraseOp declarations
//===----------------------------------------------------------------------===//

class EraseOpAdaptor {
public:
  EraseOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  EraseOpAdaptor(EraseOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getOpValue();
  ::mlir::Value opValue();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class EraseOp : public ::mlir::Op<EraseOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::HasParent<pdl::RewriteOp>::Impl, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = EraseOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.erase");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::OperationType> getOpValue();
  ::mlir::TypedValue<::mlir::pdl::OperationType> opValue();
  ::mlir::MutableOperandRange getOpValueMutable();
  ::mlir::MutableOperandRange opValueMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value opValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value opValue);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::EraseOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::OperandOp declarations
//===----------------------------------------------------------------------===//

class OperandOpAdaptor {
public:
  OperandOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  OperandOpAdaptor(OperandOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getValueType();
  ::mlir::Value valueType();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class OperandOp : public ::mlir::Op<OperandOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::pdl::ValueType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::HasParent<pdl::PatternOp>::Impl, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = OperandOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.operand");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getValueType();
  ::mlir::Value valueType();
  ::mlir::MutableOperandRange getValueTypeMutable();
  ::mlir::MutableOperandRange valueTypeMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::ValueType> getValue();
  ::mlir::TypedValue<::mlir::pdl::ValueType> value();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type value, /*optional*/::mlir::Value valueType);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::Value valueType);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::OperandOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::OperandsOp declarations
//===----------------------------------------------------------------------===//

class OperandsOpAdaptor {
public:
  OperandsOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  OperandsOpAdaptor(OperandsOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getValueType();
  ::mlir::Value valueType();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class OperandsOp : public ::mlir::Op<OperandsOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::pdl::RangeType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::HasParent<pdl::PatternOp>::Impl, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = OperandsOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.operands");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::RangeType> getValueType();
  ::mlir::TypedValue<::mlir::pdl::RangeType> valueType();
  ::mlir::MutableOperandRange getValueTypeMutable();
  ::mlir::MutableOperandRange valueTypeMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::RangeType> getValue();
  ::mlir::TypedValue<::mlir::pdl::RangeType> value();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type value, /*optional*/::mlir::Value valueType);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::Value valueType);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::OperandsOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::OperationOp declarations
//===----------------------------------------------------------------------===//

class OperationOpAdaptor {
public:
  OperationOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  OperationOpAdaptor(OperationOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getOperandValues();
  ::mlir::ValueRange operandValues();
  ::mlir::ValueRange getAttributeValues();
  ::mlir::ValueRange attributeValues();
  ::mlir::ValueRange getTypeValues();
  ::mlir::ValueRange typeValues();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getOpNameAttr();
  ::llvm::Optional< ::llvm::StringRef > getOpName();
  ::mlir::StringAttr opNameAttr();
  ::llvm::Optional< ::llvm::StringRef > opName();
  ::mlir::ArrayAttr getAttributeValueNamesAttr();
  ::mlir::ArrayAttr getAttributeValueNames();
  ::mlir::ArrayAttr attributeValueNamesAttr();
  ::mlir::ArrayAttr attributeValueNames();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class OperationOp : public ::mlir::Op<OperationOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::pdl::OperationType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::AttrSizedOperandSegments, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = OperationOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("attributeValueNames"), ::llvm::StringRef("opName"), ::llvm::StringRef("operand_segment_sizes")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getAttributeValueNamesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getAttributeValueNamesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr attributeValueNamesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr attributeValueNamesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getOpNameAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getOpNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr opNameAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr opNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getOperandSegmentSizesAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getOperandSegmentSizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr operand_segment_sizesAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr operand_segment_sizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.operation");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getOperandValues();
  ::mlir::Operation::operand_range operandValues();
  ::mlir::Operation::operand_range getAttributeValues();
  ::mlir::Operation::operand_range attributeValues();
  ::mlir::Operation::operand_range getTypeValues();
  ::mlir::Operation::operand_range typeValues();
  ::mlir::MutableOperandRange getOperandValuesMutable();
  ::mlir::MutableOperandRange operandValuesMutable();
  ::mlir::MutableOperandRange getAttributeValuesMutable();
  ::mlir::MutableOperandRange attributeValuesMutable();
  ::mlir::MutableOperandRange getTypeValuesMutable();
  ::mlir::MutableOperandRange typeValuesMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::OperationType> getOp();
  ::mlir::TypedValue<::mlir::pdl::OperationType> op();
  ::mlir::StringAttr getOpNameAttr();
  ::llvm::Optional< ::llvm::StringRef > getOpName();
  ::mlir::StringAttr opNameAttr();
  ::llvm::Optional< ::llvm::StringRef > opName();
  ::mlir::ArrayAttr getAttributeValueNamesAttr();
  ::mlir::ArrayAttr getAttributeValueNames();
  ::mlir::ArrayAttr attributeValueNamesAttr();
  ::mlir::ArrayAttr attributeValueNames();
  void setOpNameAttr(::mlir::StringAttr attr);
  void opNameAttr(::mlir::StringAttr attr);
  void setAttributeValueNamesAttr(::mlir::ArrayAttr attr);
  void attributeValueNamesAttr(::mlir::ArrayAttr attr);
  ::mlir::Attribute removeOpNameAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, Optional<StringRef> name = llvm::None, ValueRange operandValues = llvm::None, ArrayRef<StringRef> attrNames = llvm::None, ValueRange attrValues = llvm::None, ValueRange resultTypes = llvm::None);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type op, /*optional*/::mlir::StringAttr opName, ::mlir::ValueRange operandValues, ::mlir::ValueRange attributeValues, ::mlir::ArrayAttr attributeValueNames, ::mlir::ValueRange typeValues);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::StringAttr opName, ::mlir::ValueRange operandValues, ::mlir::ValueRange attributeValues, ::mlir::ArrayAttr attributeValueNames, ::mlir::ValueRange typeValues);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
  /// Returns true if the operation type referenced supports result type
  /// inference.
  bool hasTypeInference();

  /// Returns true if the operation type referenced might support result type
  /// inference, i.e. it supports type reference or is currently not
  /// registered in the context. Returns false if the root operation name
  /// has not been set.
  bool mightHaveTypeInference();
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::OperationOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::PatternOp declarations
//===----------------------------------------------------------------------===//

class PatternOpAdaptor {
public:
  PatternOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  PatternOpAdaptor(PatternOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::IntegerAttr getBenefitAttr();
  uint16_t getBenefit();
  ::mlir::IntegerAttr benefitAttr();
  uint16_t benefit();
  ::mlir::StringAttr getSymNameAttr();
  ::llvm::Optional< ::llvm::StringRef > getSymName();
  ::mlir::StringAttr sym_nameAttr();
  ::llvm::Optional< ::llvm::StringRef > sym_name();
  ::mlir::RegionRange getRegions();
  ::mlir::Region &getBodyRegion();
  ::mlir::Region &bodyRegion();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class PatternOp : public ::mlir::Op<PatternOp, ::mlir::OpTrait::OneRegion, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::SingleBlock, ::mlir::OpTrait::OpInvariants, ::mlir::OpTrait::IsIsolatedFromAbove, ::mlir::SymbolOpInterface::Trait, ::mlir::OpAsmOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = PatternOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("benefit"), ::llvm::StringRef("sym_name")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getBenefitAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getBenefitAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr benefitAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr benefitAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getSymNameAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getSymNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr sym_nameAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr sym_nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.pattern");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Region &getBodyRegion();
  ::mlir::Region &bodyRegion();
  ::mlir::IntegerAttr getBenefitAttr();
  uint16_t getBenefit();
  ::mlir::IntegerAttr benefitAttr();
  uint16_t benefit();
  ::mlir::StringAttr getSymNameAttr();
  ::llvm::Optional< ::llvm::StringRef > getSymName();
  ::mlir::StringAttr sym_nameAttr();
  ::llvm::Optional< ::llvm::StringRef > sym_name();
  void setBenefitAttr(::mlir::IntegerAttr attr);
  void benefitAttr(::mlir::IntegerAttr attr);
  void setSymNameAttr(::mlir::StringAttr attr);
  void sym_nameAttr(::mlir::StringAttr attr);
  ::mlir::Attribute removeSym_nameAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, Optional<uint16_t> benefit = 1, Optional<StringRef> name = llvm::None);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::IntegerAttr benefit, /*optional*/::mlir::StringAttr sym_name);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::IntegerAttr benefit, /*optional*/::mlir::StringAttr sym_name);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, uint16_t benefit, /*optional*/::mlir::StringAttr sym_name);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, uint16_t benefit, /*optional*/::mlir::StringAttr sym_name);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verifyRegions();
  static ::llvm::StringRef getDefaultDialect();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
  //===------------------------------------------------------------------===//
  // SymbolOpInterface Methods
  //===------------------------------------------------------------------===//

  /// A PatternOp may optionally define a symbol.
  bool isOptionalSymbol() { return true; }

  /// Returns the rewrite operation of this pattern.
  RewriteOp getRewriter();
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::PatternOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::ReplaceOp declarations
//===----------------------------------------------------------------------===//

class ReplaceOpAdaptor {
public:
  ReplaceOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ReplaceOpAdaptor(ReplaceOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getOpValue();
  ::mlir::Value opValue();
  ::mlir::Value getReplOperation();
  ::mlir::Value replOperation();
  ::mlir::ValueRange getReplValues();
  ::mlir::ValueRange replValues();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class ReplaceOp : public ::mlir::Op<ReplaceOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<1>::Impl, ::mlir::OpTrait::AttrSizedOperandSegments, ::mlir::OpTrait::HasParent<pdl::RewriteOp>::Impl, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ReplaceOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("operand_segment_sizes")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getOperandSegmentSizesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getOperandSegmentSizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr operand_segment_sizesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr operand_segment_sizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.replace");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::OperationType> getOpValue();
  ::mlir::TypedValue<::mlir::pdl::OperationType> opValue();
  ::mlir::Value getReplOperation();
  ::mlir::Value replOperation();
  ::mlir::Operation::operand_range getReplValues();
  ::mlir::Operation::operand_range replValues();
  ::mlir::MutableOperandRange getOpValueMutable();
  ::mlir::MutableOperandRange opValueMutable();
  ::mlir::MutableOperandRange getReplOperationMutable();
  ::mlir::MutableOperandRange replOperationMutable();
  ::mlir::MutableOperandRange getReplValuesMutable();
  ::mlir::MutableOperandRange replValuesMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value opValue, /*optional*/::mlir::Value replOperation, ::mlir::ValueRange replValues);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value opValue, /*optional*/::mlir::Value replOperation, ::mlir::ValueRange replValues);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::ReplaceOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::ResultOp declarations
//===----------------------------------------------------------------------===//

class ResultOpAdaptor {
public:
  ResultOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ResultOpAdaptor(ResultOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getParent();
  ::mlir::Value parent();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::IntegerAttr getIndexAttr();
  uint32_t getIndex();
  ::mlir::IntegerAttr indexAttr();
  uint32_t index();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class ResultOp : public ::mlir::Op<ResultOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::pdl::ValueType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ResultOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("index")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getIndexAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getIndexAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr indexAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr indexAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.result");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::OperationType> getParent();
  ::mlir::TypedValue<::mlir::pdl::OperationType> parent();
  ::mlir::MutableOperandRange getParentMutable();
  ::mlir::MutableOperandRange parentMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::ValueType> getVal();
  ::mlir::TypedValue<::mlir::pdl::ValueType> val();
  ::mlir::IntegerAttr getIndexAttr();
  uint32_t getIndex();
  ::mlir::IntegerAttr indexAttr();
  uint32_t index();
  void setIndexAttr(::mlir::IntegerAttr attr);
  void indexAttr(::mlir::IntegerAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type val, ::mlir::Value parent, ::mlir::IntegerAttr index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value parent, ::mlir::IntegerAttr index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type val, ::mlir::Value parent, uint32_t index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value parent, uint32_t index);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::ResultOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::ResultsOp declarations
//===----------------------------------------------------------------------===//

class ResultsOpAdaptor {
public:
  ResultsOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ResultsOpAdaptor(ResultsOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getParent();
  ::mlir::Value parent();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::IntegerAttr getIndexAttr();
  ::llvm::Optional<uint32_t> getIndex();
  ::mlir::IntegerAttr indexAttr();
  ::llvm::Optional<uint32_t> index();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class ResultsOp : public ::mlir::Op<ResultsOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::pdl::PDLType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ResultsOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("index")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getIndexAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getIndexAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr indexAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr indexAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.results");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::OperationType> getParent();
  ::mlir::TypedValue<::mlir::pdl::OperationType> parent();
  ::mlir::MutableOperandRange getParentMutable();
  ::mlir::MutableOperandRange parentMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::PDLType> getVal();
  ::mlir::TypedValue<::mlir::pdl::PDLType> val();
  ::mlir::IntegerAttr getIndexAttr();
  ::llvm::Optional<uint32_t> getIndex();
  ::mlir::IntegerAttr indexAttr();
  ::llvm::Optional<uint32_t> index();
  void setIndexAttr(::mlir::IntegerAttr attr);
  void indexAttr(::mlir::IntegerAttr attr);
  ::mlir::Attribute removeIndexAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type val, ::mlir::Value parent, /*optional*/::mlir::IntegerAttr index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value parent, /*optional*/::mlir::IntegerAttr index);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::ResultsOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::RewriteOp declarations
//===----------------------------------------------------------------------===//

class RewriteOpAdaptor {
public:
  RewriteOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  RewriteOpAdaptor(RewriteOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getRoot();
  ::mlir::Value root();
  ::mlir::ValueRange getExternalArgs();
  ::mlir::ValueRange externalArgs();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::StringAttr getNameAttr();
  ::llvm::Optional< ::llvm::StringRef > getName();
  ::mlir::StringAttr nameAttr();
  ::llvm::Optional< ::llvm::StringRef > name();
  ::mlir::RegionRange getRegions();
  ::mlir::Region &getBodyRegion();
  ::mlir::Region &bodyRegion();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class RewriteOp : public ::mlir::Op<RewriteOp, ::mlir::OpTrait::OneRegion, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::HasParent<pdl::PatternOp>::Impl, ::mlir::OpTrait::NoTerminator, ::mlir::OpTrait::NoRegionArguments, ::mlir::OpTrait::SingleBlock, ::mlir::OpTrait::AttrSizedOperandSegments, ::mlir::OpTrait::OpInvariants, ::mlir::OpTrait::IsTerminator, ::mlir::OpAsmOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = RewriteOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("name"), ::llvm::StringRef("operand_segment_sizes")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getNameAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getNameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr nameAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr nameAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getOperandSegmentSizesAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getOperandSegmentSizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr operand_segment_sizesAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr operand_segment_sizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.rewrite");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getRoot();
  ::mlir::Value root();
  ::mlir::Operation::operand_range getExternalArgs();
  ::mlir::Operation::operand_range externalArgs();
  ::mlir::MutableOperandRange getRootMutable();
  ::mlir::MutableOperandRange rootMutable();
  ::mlir::MutableOperandRange getExternalArgsMutable();
  ::mlir::MutableOperandRange externalArgsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Region &getBodyRegion();
  ::mlir::Region &bodyRegion();
  ::mlir::StringAttr getNameAttr();
  ::llvm::Optional< ::llvm::StringRef > getName();
  ::mlir::StringAttr nameAttr();
  ::llvm::Optional< ::llvm::StringRef > name();
  void setNameAttr(::mlir::StringAttr attr);
  void nameAttr(::mlir::StringAttr attr);
  ::mlir::Attribute removeNameAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, /*optional*/::mlir::Value root, /*optional*/::mlir::StringAttr name, ::mlir::ValueRange externalArgs);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::Value root, /*optional*/::mlir::StringAttr name, ::mlir::ValueRange externalArgs);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verifyRegions();
  static ::llvm::StringRef getDefaultDialect();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::RewriteOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::TypeOp declarations
//===----------------------------------------------------------------------===//

class TypeOpAdaptor {
public:
  TypeOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  TypeOpAdaptor(TypeOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::TypeAttr getConstantTypeAttr();
  ::llvm::Optional<::mlir::Type> getConstantType();
  ::mlir::TypeAttr constantTypeAttr();
  ::llvm::Optional<::mlir::Type> constantType();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class TypeOp : public ::mlir::Op<TypeOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::pdl::TypeType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = TypeOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("constantType")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getConstantTypeAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getConstantTypeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr constantTypeAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr constantTypeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.type");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::TypeType> getResult();
  ::mlir::TypedValue<::mlir::pdl::TypeType> result();
  ::mlir::TypeAttr getConstantTypeAttr();
  ::llvm::Optional<::mlir::Type> getConstantType();
  ::mlir::TypeAttr constantTypeAttr();
  ::llvm::Optional<::mlir::Type> constantType();
  void setConstantTypeAttr(::mlir::TypeAttr attr);
  void constantTypeAttr(::mlir::TypeAttr attr);
  ::mlir::Attribute removeConstantTypeAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, /*optional*/::mlir::TypeAttr constantType);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::TypeAttr constantType);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::TypeOp)

namespace mlir {
namespace pdl {

//===----------------------------------------------------------------------===//
// ::mlir::pdl::TypesOp declarations
//===----------------------------------------------------------------------===//

class TypesOpAdaptor {
public:
  TypesOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  TypesOpAdaptor(TypesOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::ArrayAttr getConstantTypesAttr();
  ::llvm::Optional< ::mlir::ArrayAttr > getConstantTypes();
  ::mlir::ArrayAttr constantTypesAttr();
  ::llvm::Optional< ::mlir::ArrayAttr > constantTypes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class TypesOp : public ::mlir::Op<TypesOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::pdl::RangeType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = TypesOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("constantTypes")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getConstantTypesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getConstantTypesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr constantTypesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr constantTypesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("pdl.types");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::pdl::RangeType> getResult();
  ::mlir::TypedValue<::mlir::pdl::RangeType> result();
  ::mlir::ArrayAttr getConstantTypesAttr();
  ::llvm::Optional< ::mlir::ArrayAttr > getConstantTypes();
  ::mlir::ArrayAttr constantTypesAttr();
  ::llvm::Optional< ::mlir::ArrayAttr > constantTypes();
  void setConstantTypesAttr(::mlir::ArrayAttr attr);
  void constantTypesAttr(::mlir::ArrayAttr attr);
  ::mlir::Attribute removeConstantTypesAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, /*optional*/::mlir::ArrayAttr constantTypes);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, /*optional*/::mlir::ArrayAttr constantTypes);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace pdl
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::pdl::TypesOp)


#endif  // GET_OP_CLASSES

