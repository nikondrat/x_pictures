import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'generate_resp.g.dart';

@JsonSerializable()
class GenerateResponse {
  @JsonKey()
  final String id;

  @JsonKey()
  final Status status;

  @JsonKey()
  final String? content;

  @JsonKey(name: 'estimated_time')
  final int? estimatedTime;

  @JsonKey(
    name: 'estimated_timestamp',
    fromJson: _dateTimeFromTimestamp,
  )
  final DateTime estimatedTimestamp;

  @JsonKey(name: 'is_blur')
  final bool isBlur;

  @JsonKey(name: 'user_balance', fromJson: _userBalanceFromJson)
  final double userBalance;

  @JsonKey(name: 'updated')
  final DateTime updatedDate;

  @JsonKey(name: 'created')
  final DateTime createdDate;

  GenerateResponse({
    required this.id,
    required this.status,
    required this.content,
    required this.estimatedTime,
    required this.estimatedTimestamp,
    required this.isBlur,
    required this.userBalance,
    required this.updatedDate,
    required this.createdDate,
  });

  factory GenerateResponse.fromJson(Map<String, dynamic> json) =>
      _$GenerateResponseFromJson(json);

  Map<String, dynamic> toJson() => _$GenerateResponseToJson(this);

  static double _userBalanceFromJson(String json) => double.parse(json);

  static DateTime _dateTimeFromTimestamp(int timestamp) =>
      DateTime.fromMillisecondsSinceEpoch(timestamp * 1000);
}
