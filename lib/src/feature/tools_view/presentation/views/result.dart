import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/data.dart';

class ImageWithBackgroundResultView extends StatelessWidget {
  const ImageWithBackgroundResultView({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;
    final bool isPro = false;

    final PacksStore store = Provider.of<PacksStore>(context);

    return Scaffold(
      appBar: AppBar(title: Text(store.selected.title)),
      body: AppBody(
        builder: (windowWidth, windowHeight, windowSize) {
          return SingleChildScrollView(
            child: Padding(
              padding: HorizontalSpacing.centered(windowWidth),
              child: Column(
                children: [
                  GridView.count(
                      shrinkWrap: true,
                      crossAxisCount: 2,
                      crossAxisSpacing: AppValues.kPadding,
                      mainAxisSpacing: AppValues.kPadding,
                      childAspectRatio: .6,
                      children: [
                        ItemModel(
                            title: t.backgrounds.types.texture.types.wood,
                            url:
                                'https://i.pinimg.com/originals/89/c3/be/89c3beddf3c836e9b04430020d9cf32b.jpg'),
                        ItemModel(
                            title: t.backgrounds.types.texture.types.wood,
                            url:
                                'https://i.pinimg.com/originals/89/c3/be/89c3beddf3c836e9b04430020d9cf32b.jpg'),
                        ItemModel(
                            title: t.backgrounds.types.texture.types.wood,
                            url:
                                'https://i.pinimg.com/originals/89/c3/be/89c3beddf3c836e9b04430020d9cf32b.jpg'),
                        ItemModel(
                            title: t.backgrounds.types.texture.types.wood,
                            url:
                                'https://i.pinimg.com/originals/89/c3/be/89c3beddf3c836e9b04430020d9cf32b.jpg'),
                      ].mapIndexed((i, e) {
                        return Stack(
                          fit: StackFit.expand,
                          children: [
                            ClipRRect(
                              borderRadius:
                                  BorderRadius.circular(AppValues.kRadius),
                              child: CachedNetworkImage(
                                imageUrl: store.selected!.images[0].url,
                                fit: BoxFit.cover,
                              ),
                            ),
                            if (!isPro && i != 0)
                              Align(
                                  alignment: Alignment.topRight,
                                  child: Padding(
                                    padding: const EdgeInsets.all(
                                        AppValues.kPadding / 2),
                                    child: SvgPicture.asset(Assets.icons.pro),
                                  ))
                          ],
                        );
                      }).toList()),
                  const Gap(AppValues.kPadding),
                  isPro
                      ? Row(
                          children: [
                            Expanded(
                              child: FilledButton.icon(
                                onPressed: () {},
                                label: AutoSizeText(
                                  t.generateView.repeat,
                                  style: textTheme.titleLarge!.copyWith(
                                      color: colorScheme.onSecondary,
                                      fontWeight: FontWeight.bold),
                                ),
                                icon: SvgPicture.asset(Assets.icons.generate),
                                style: ButtonStyle(
                                    padding: const WidgetStatePropertyAll(
                                        EdgeInsets.symmetric(
                                            horizontal: AppValues.kPadding,
                                            vertical:
                                                AppValues.kPadding * 1.5)),
                                    backgroundColor: WidgetStatePropertyAll(
                                        colorScheme.secondary)),
                              ),
                            ),
                          ],
                        )
                      : GradientButton(
                          onPressed: () {},
                          text: t.toolsView.unlock,
                        )
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
