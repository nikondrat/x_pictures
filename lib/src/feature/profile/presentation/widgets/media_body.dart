import 'package:flutter/widgets.dart';
import 'package:gap/gap.dart';
import 'package:grouped_list/grouped_list.dart';
import 'package:x_pictures/src/data.dart';

class MediaBody extends StatelessWidget {
  final List<MediaModel> items;
  const MediaBody({super.key, required this.items});

  @override
  Widget build(BuildContext context) {
    return GroupedListView(
      elements: items,
      shrinkWrap: true,
      groupBy: (element) => element.createdDate,
      groupSeparatorBuilder: (groupBy) => const Gap(AppValues.kPadding),
      itemBuilder: (context, element) => MediaItem(model: element),
      itemComparator: (item1, item2) =>
          item1.createdDate.compareTo(item2.createdDate),
      order: GroupedListOrder.ASC,
      useStickyGroupSeparators: true,
    );
  }
}
