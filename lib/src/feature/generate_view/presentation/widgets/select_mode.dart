import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class SelectModeWidget extends StatelessWidget {
  const SelectModeWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final GenerateViewStore store = Provider.of<GenerateViewStore>(context);

    return Observer(builder: (context) {
      return SizedBox(
        height: 30.h,
        child: Row(
          children: [
            Expanded(
                child: _Tab(
              onTap: () => store.setSelected(0),
              title: t.generateView.type.images,
              isSelected: store.selected == 0,
            )),
            Expanded(
                child: _Tab(
              onTap: () => store.setSelected(1),
              title: t.generateView.type.video,
              isSelected: store.selected == 1,
            )),
          ],
        ),
      );
    });
  }
}

class _Tab extends StatelessWidget {
  final Function() onTap;
  final String title;
  final bool isSelected;
  const _Tab(
      {required this.onTap, required this.title, required this.isSelected});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return isSelected
        ? GradientButton(
            onPressed: onTap,
            text: title,
            padding:
                const EdgeInsets.symmetric(vertical: AppValues.kPadding / 3),
            textStyle: textTheme.bodyMedium,
          )
        : Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Expanded(
                child: TextButton(
                  onPressed: onTap,
                  style: const ButtonStyle(
                      shape: WidgetStatePropertyAll(RoundedRectangleBorder(
                          borderRadius: BorderRadius.all(
                              Radius.circular(AppValues.kRadius)))),
                      backgroundColor:
                          WidgetStatePropertyAll(AppColors.kAdditionalColor)),
                  child: AutoSizeText(
                    title,
                    style: textTheme.bodyMedium!
                        .copyWith(color: colorScheme.onSurface),
                  ),
                ),
              ),
            ],
          );
  }
}
