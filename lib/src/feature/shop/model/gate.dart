import 'package:json_annotation/json_annotation.dart';

part 'gate.g.dart';

@JsonSerializable()
class Gate {
  @JsonKey()
  final String id;

  @JsonKey()
  final String label;

  Gate({
    required this.id,
    required this.label,
  });

  factory Gate.fromJson(Map<String, dynamic> json) => _$GateFromJson(json);

  Map<String, dynamic> toJson() => _$GateToJson(this);
}
