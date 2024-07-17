import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'user.g.dart';

enum ProfileType {
  @JsonValue('basic')
  basic,
  @JsonValue('advance')
  advance,
  @JsonValue('premium')
  premium,
  @JsonValue('super_premium')
  superPremium,
}

@JsonSerializable()
class User {
  @JsonKey()
  final String id;

  @JsonKey()
  final String? username;

  @JsonKey()
  final String email;

  @JsonKey(name: 'image')
  final String? imageUrl;

  @JsonKey(name: 'balance')
  final String balance;

  @JsonKey(name: 'type')
  final ProfileType profileType;

  @JsonKey(name: 'type_verbose')
  final String typeVerbose;

  @JsonKey(name: 'is_verified')
  final bool isVerified;

  @JsonKey(name: 'subscription')
  final Subscription? subscription;

  @JsonKey(name: 'updated')
  final DateTime updated;

  @JsonKey(name: 'created')
  final DateTime created;

  User(
      {required this.id,
      required this.username,
      required this.email,
      required this.imageUrl,
      required this.balance,
      required this.profileType,
      required this.typeVerbose,
      required this.isVerified,
      required this.subscription,
      required this.updated,
      required this.created});

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

  Map<String, dynamic> toJson() => _$UserToJson(this);
}
