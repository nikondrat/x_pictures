import 'package:json_annotation/json_annotation.dart';

part 'product.g.dart';

enum ProductType {
  @JsonValue('subscription')
  subscription,
  @JsonValue('one-time')
  oneTime,
}

@JsonSerializable()
class Product {
  @JsonKey()
  final int id;

  @JsonKey()
  final String title;

  @JsonKey()
  final String description;

  @JsonKey(name: 'image')
  final String imageUrl;

  @JsonKey()
  final String price;

  @JsonKey()
  final String currency;

  @JsonKey()
  final ProductType type;

  @JsonKey()
  final String amount;

  @JsonKey()
  final int lifetime;

  @JsonKey(name: 'lifetime_type')
  final String lifetimeType;

  @JsonKey(name: 'paypal_billing_plan_id')
  final String paypalBillingPlanId;

  Product({
    required this.id,
    required this.title,
    required this.description,
    required this.imageUrl,
    required this.price,
    required this.currency,
    required this.type,
    required this.amount,
    required this.lifetime,
    required this.lifetimeType,
    required this.paypalBillingPlanId,
  });

  factory Product.fromJson(Map<String, dynamic> json) =>
      _$ProductFromJson(json);

  Map<String, dynamic> toJson() => _$ProductToJson(this);
}
