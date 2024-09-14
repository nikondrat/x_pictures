import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'orders_body.g.dart';

@JsonSerializable()
class OrdersBody extends PageModel {
  @JsonKey(name: 'results')
  final List<Order> orders;

  OrdersBody({
    required super.count,
    required super.total,
    required super.nextUrl,
    required super.previousUrl,
    required this.orders,
  });

  factory OrdersBody.fromJson(Map<String, dynamic> json) =>
      _$OrdersBodyFromJson(json);

  /// Connect the generated [_$OrdersBodyToJson] function to the `toJson` method.
  @override
  Map<String, dynamic> toJson() => _$OrdersBodyToJson(this);
}
