import 'package:auto_size_text/auto_size_text.dart';
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class _Format {
  final double width;
  final double height;
  _Format({required this.width, required this.height});
}

class GenerateFormats extends StatelessWidget {
  final double windowHeight;
  const GenerateFormats({super.key, required this.windowHeight});

  @override
  Widget build(BuildContext context) {
    final GenerateViewStore store = Provider.of<GenerateViewStore>(context);

    final List<_Format> formats = [
      _Format(width: 2, height: 3),
      _Format(width: 3, height: 2),
      _Format(width: 1, height: 1),
      _Format(width: 9, height: 6),
      _Format(width: 16, height: 9),
    ];

    return TitleWithBody(
      title: t.generateView.format,
      action: ResetButton(
        onPressed: () {
          store.setSelectedFormat(0);
        },
      ),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: LayoutBuilder(builder: (context, size) {
          return Row(
            children: formats
                .mapIndexed((i, e) => Observer(builder: (context) {
                      return GestureDetector(
                        onTap: () {
                          store.setSelectedFormat(i);
                        },
                        child: _FormatWidget(
                          format: e,
                          isSelected: i == store.selectedFormat,
                          windowHeight: windowHeight,
                        ),
                      );
                    }))
                .toList(),
          );
        }),
      ),
    );
  }
}

class _FormatWidget extends StatelessWidget {
  final _Format format;
  final double windowHeight;
  final bool isSelected;

  const _FormatWidget({
    required this.format,
    required this.windowHeight,
    required this.isSelected,
  });

  @override
  Widget build(BuildContext context) {
    final themeData = Theme.of(context);
    final textTheme = themeData.textTheme;
    final colorScheme = themeData.colorScheme;

    final double fixedWidth = windowHeight * .07;
    final bool isSquare = format.width == format.height;
    final double height =
        isSquare ? fixedWidth : (format.height / format.width) * 60;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppValues.kPadding / 4),
      child: SizedBox(
        width: fixedWidth,
        height: height,
        child: Container(
          decoration: BoxDecoration(
            border: Border.all(
              color: isSelected ? colorScheme.primary : AppColors.kOutlineColor,
            ),
            borderRadius: BorderRadius.circular(AppValues.kRadius),
          ),
          child: Center(
            child: AutoSizeText(
              '${format.width.toInt()}:${format.height.toInt()}',
              style: textTheme.bodyLarge?.copyWith(
                color: colorScheme.secondary,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
