import 'package:json_annotation/json_annotation.dart';

part 'patreon.g.dart';

@JsonSerializable()
class Patreon {
  @JsonKey(name: 'is_connected')
  final bool isConnected;
  @JsonKey(name: 'is_activated')
  final bool isActivated;
  @JsonKey(name: 'is_member')
  final bool isMember;

  Patreon({
    required this.isConnected,
    required this.isActivated,
    required this.isMember,
  });

  factory Patreon.fromJson(Map<String, dynamic> json) =>
      _$PatreonFromJson(json);

  Map<String, dynamic> toJson() => _$PatreonToJson(this);
}
