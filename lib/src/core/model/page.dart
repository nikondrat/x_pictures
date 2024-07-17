import 'package:json_annotation/json_annotation.dart';

import 'package:mobx/mobx.dart';

part 'page.g.dart';

@JsonSerializable()
class PageModel extends _PageModel with _$PageModel {
  @JsonKey()
  final int count;

  @JsonKey(name: 'num_pages')
  final int total;

  @JsonKey(name: 'next')
  final String? nextUrl;

  @JsonKey(name: 'previous')
  final String? previousUrl;

  PageModel({
    required this.count,
    required this.total,
    required this.nextUrl,
    required this.previousUrl,
  });

  factory PageModel.fromJson(Map<String, dynamic> json) =>
      _$PageModelFromJson(json);

  /// Connect the generated [_$PageModelToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$PageModelToJson(this);
}

abstract class _PageModel with Store {
  _PageModel();

  @observable
  @JsonKey(includeToJson: false, includeFromJson: false)
  int selectedPage = 0;

  @action
  void selectPage(int index) {
    selectedPage = index;
  }
}
