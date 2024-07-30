import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:provider/provider.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/core/constant/icons.dart';
import 'package:x_pictures/src/data.dart';

class BottomNavBarControllerPage extends StatefulWidget {
  const BottomNavBarControllerPage({super.key});

  @override
  State<BottomNavBarControllerPage> createState() =>
      _BottomNavBarControllerPageState();
}

class _BottomNavBarControllerPageState
    extends State<BottomNavBarControllerPage> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    final List<Widget> pages = [
      const HomeView(),
      const GenerateView(),
      ProfileView(
        goHome: () {
          setState(() {
            _selectedIndex = 0;
          });
        },
        goGenerate: () {
          setState(() {
            _selectedIndex = 1;
          });
        },
        selectedIndex: _selectedIndex,
      )
    ];
    final HomeStore store = context.read();

    return Scaffold(
        backgroundColor: Colors.transparent,
        bottomNavigationBar: Observer(builder: (context) {
          return !store.showBottomBar
              ? const BottomBarPhotosFuncs()
              : ClipRRect(
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(20.r),
                    topRight: Radius.circular(20.r),
                  ),
                  child: BottomNavigationBar(
                    currentIndex: _selectedIndex,
                    onTap: (index) {
                      setState(() {
                        _selectedIndex = index;
                      });
                    },
                    backgroundColor: const Color(0xff0D1120),
                    selectedItemColor: Colors.orange[900],
                    selectedLabelStyle: TextStyle(
                      fontSize: 6.sp,
                      fontWeight: FontWeight.w700,
                    ),
                    selectedIconTheme: IconThemeData(
                      color: Colors.orange[900],
                    ),
                    unselectedIconTheme: const IconThemeData(
                      color: Color(0xff6F6F72),
                    ),
                    unselectedLabelStyle: TextStyle(
                      fontSize: 6.sp,
                      fontWeight: FontWeight.w400,
                      color: const Color(0xff6F6F72),
                    ),
                    unselectedItemColor: const Color(0xff6F6F72),
                    // iconSize: 40,
                    items: [
                      BottomNavigationBarItem(
                        icon: SvgPicture.asset(
                          Assets.icons.home,
                          color: _selectedIndex == 0
                              ? Colors.orange[900]
                              : const Color(0xff6F6F72),
                        ),
                        label: 'Home',
                      ),
                      BottomNavigationBarItem(
                        icon: SvgPicture.asset(
                          AppIcons.generateIcon,
                          color: _selectedIndex == 1
                              ? Colors.orange[900]
                              : const Color(0xff6F6F72),
                        ),
                        label: 'Generate',
                      ),
                      BottomNavigationBarItem(
                        icon: Icon(
                          Icons.account_circle_outlined,
                          color: _selectedIndex == 2
                              ? Colors.orange[900]
                              : const Color(0xff6F6F72),
                        ),
                        label: 'My Profile',
                      ),
                    ],
                  ),
                );
        }),
        body: pages[_selectedIndex]);
  }
}
