import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'order.g.dart';

@JsonSerializable()
class Order {
  @JsonKey()
  final String id;

  @JsonKey(name: 'payment_url')
  final String paymentUrl;

  @JsonKey()
  final Product product;

  @JsonKey()
  final String price;

  @JsonKey()
  final String currency;

  @JsonKey()
  final String gateway;

  @JsonKey()
  final Status status;

  @JsonKey(name: 'expiry_at')
  final DateTime expiryDate;

  @JsonKey(name: 'updated')
  final DateTime updatedDate;

  @JsonKey(name: 'created')
  final DateTime createdDate;

  Order({
    required this.id,
    required this.paymentUrl,
    required this.product,
    required this.price,
    required this.currency,
    required this.gateway,
    required this.status,
    required this.expiryDate,
    required this.updatedDate,
    required this.createdDate,
  });

  factory Order.fromJson(Map<String, dynamic> json) => _$OrderFromJson(json);

  Map<String, dynamic> toJson() => _$OrderToJson(this);
}
