import 'package:json_annotation/json_annotation.dart';

enum Status {
  @JsonValue(0)
  created,
  @JsonValue(1)
  processing,
  @JsonValue(2)
  completed,
  @JsonValue(-1)
  failed
}
