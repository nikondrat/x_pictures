import 'package:json_annotation/json_annotation.dart';

part 'subscription.g.dart';

@JsonSerializable()
class Subscription {
  @JsonKey()
  final String id;

  @JsonKey()
  final String title;

  @JsonKey(name: 'is_active')
  final bool isActive;

  @JsonKey(name: 'start_period')
  final DateTime startDate;

  @JsonKey(name: 'end_period')
  final DateTime endDate;

  Subscription(
      {required this.id,
      required this.title,
      required this.isActive,
      required this.startDate,
      required this.endDate});

  factory Subscription.fromJson(Map<String, dynamic> json) =>
      _$SubscriptionFromJson(json);

  Map<String, dynamic> toJson() => _$SubscriptionToJson(this);
}
