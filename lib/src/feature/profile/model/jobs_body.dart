import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'jobs_body.g.dart';

@JsonSerializable()
class JobsBody extends PageModel {
  JobsBody(
      {required super.count,
      required super.total,
      required super.nextUrl,
      required super.previousUrl,
      required this.jobs});

  @JsonKey(name: 'results')
  final List<JobModel> jobs;

  factory JobsBody.fromJson(Map<String, dynamic> json) =>
      _$JobsBodyFromJson(json);

  /// Connect the generated [_$JobsBodyToJson] function to the `toJson` method.
  @override
  Map<String, dynamic> toJson() => _$JobsBodyToJson(this);
}
