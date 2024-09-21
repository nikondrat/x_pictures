import 'dart:math';

import 'package:animated_toggle_switch/animated_toggle_switch.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class SelectModeWidget extends StatelessWidget {
  const SelectModeWidget({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final GenerateViewStore store = context.watch<GenerateViewStore>();

    return Observer(builder: (context) {
      return Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Expanded(
            child: AnimatedToggleSwitch<int>.size(
              current: min(store.selected, 2),
              iconOpacity: 1.0,
              selectedIconScale: 1.0,
              style: ToggleStyle(
                backgroundColor: AppColors.kSecondaryAdditionallyColor,
                indicatorColor: AppColors.kPrimaryColor,
                borderRadius: BorderRadius.circular(10.0),
              ),
              values: const [0, 1],
              height: 40,
              indicatorSize: const Size.fromWidth(200),
              iconAnimationType: AnimationType.onHover,
              styleAnimationType: AnimationType.onSelected,
              customIconBuilder: (context, local, global) {
                final text = [
                  t.generateView.type.images,
                  t.generateView.type.video,
                ][local.index];
                return Center(
                    child: Text(text,
                        style:
                            const TextStyle(color: AppColors.kSecondaryColor)));
              },
              borderWidth: 0,
              onChanged: (i) {
                store.setSelected(i);
              },
            ),
          )
        ],
      );
    });
  }
}
