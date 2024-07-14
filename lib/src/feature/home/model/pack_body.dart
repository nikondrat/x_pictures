import 'package:json_annotation/json_annotation.dart';

import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'pack_body.g.dart';

@JsonSerializable()
class PackBody extends _PackBody with _$PackBody {
  @JsonKey()
  final int count;

  @JsonKey(name: 'num_pages')
  final int total;

  @JsonKey(name: 'next')
  final String? nextUrl;

  @JsonKey(name: 'previous')
  final String? previousUrl;

  @JsonKey(name: 'results')
  final List<PackModel> packs;

  PackBody({
    required this.count,
    required this.total,
    required this.nextUrl,
    required this.previousUrl,
    required this.packs,
  });

  factory PackBody.fromJson(Map<String, dynamic> json) =>
      _$PackBodyFromJson(json);

  /// Connect the generated [_$PackBodyToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$PackBodyToJson(this);
}

abstract class _PackBody with Store {
  _PackBody();

  @observable
  @JsonKey(includeToJson: false, includeFromJson: false)
  int selectedPage = 0;

  @action
  void selectPage(int index) {
    selectedPage = index;
  }
}
