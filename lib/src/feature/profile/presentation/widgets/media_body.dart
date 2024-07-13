import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:grouped_grid/grouped_grid.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class MediaBody extends StatelessWidget {
  const MediaBody({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData theme = Theme.of(context);
    final TextTheme textTheme = theme.textTheme;
    final MediaBodyStore store = context.read<MediaBodyStore>();

    return GroupedGridView(
      gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
          crossAxisSpacing: AppValues.kPadding,
          mainAxisSpacing: AppValues.kPadding,
          maxCrossAxisExtent: 200,
          childAspectRatio: .6),
      groupKeys: store.groupedItems.keys,
      itemBuilder: (context, group) {
        MediaModel model = store.groupedItems[group.key]![group.itemIndex];
        return MediaItem(model: model);
      },
      itemCountForGroup: (group) => store.groupedItems[group]?.length ?? 0,
      groupHeaderBuilder: (context, key) {
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: AppValues.kPadding),
          child: AutoSizeText(
            t.common.now(month: t.common.months[key.month], day: key.day),
            style:
                textTheme.bodyLarge!.copyWith(color: AppColors.kOutlineColor),
          ),
        );
      },
      groupStickyHeaders: false,
    );
  }
}
